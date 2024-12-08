from django.utils import timezone
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.competition.utils.random_task import get_random
from apps.competition.utils.generators import generator_uid
from apps.competition.utils.evaluate_code import evaluate_code
from .serializers import (
    CompetitionJoinSerializer,
    CompetitionValidateSerializer,
    SubmitCodeSerializer,
)
from apps.task.models import Task

# Utility functions for common operations
def get_competition_data(comp_uid):
    competition_data = cache.get(comp_uid)
    if not competition_data:
        return None, Response(
            {"success": False, "error": "Competition not found or expired."},
            status=status.HTTP_404_NOT_FOUND,
        )
    return competition_data, None


def set_cache_data(comp_uid, competition_data):
    duration = competition_data.get("duration", 0) * 60  # Convert to seconds
    cache.set(comp_uid, competition_data, timeout=duration)


class CompetitionCreateView(APIView):
    def get(self, request):
        competition_keys = cache.keys("*")
        competitions_data = [
            cache.get(comp_uid) for comp_uid in competition_keys if cache.get(comp_uid)
        ]
        serialized_data = CompetitionValidateSerializer(
            competitions_data, many=True
        ).data
        return Response(
            {
                "success": True,
                "competitions": serialized_data,
                "message": "Competitions retrieved successfully.",
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        serializer = CompetitionValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        difficulty = serializer.validated_data.get("difficulty")
        # Replace with a random task retrieval if necessary
        task = Task.objects.filter(difficulty=difficulty).first()
        if not task:
            return Response(
                {"success": False, "message": "No task available for the specified difficulty."},
                status=status.HTTP_404_NOT_FOUND,
            )

        comp_uid = str(generator_uid())
        if cache.get(comp_uid):
            return Response(
                {"success": False, "message": "Please regenerate again!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comp_data = {
            "competition_uid": comp_uid,
            **serializer.validated_data,
            "task_title": task.title,
            "created_at": timezone.now(),
            "results": [],
        }
        set_cache_data(comp_uid, comp_data)

        task_data = {
            "id": task.id,
            "title": task.title,
            "difficulty": task.difficulty,
            "description": task.description,
            "test_cases": task.test_cases.all().values(
                "input", "output", "input_type", "output_type"
            ),
        }
        return Response(
            {
                "success": True,
                "competition_uid": comp_uid,
                "task": task_data,
                "message": "Competition created successfully.",
            },
            status=status.HTTP_201_CREATED,
        )


class JoinCompetitionView(APIView):
    def post(self, request):
        serializer = CompetitionJoinSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comp_uid = serializer.validated_data.get("comp_uid")
        nickname = serializer.data.get("nickname")

        competition_data, error_response = get_competition_data(comp_uid)
        if error_response:
            return error_response

        if nickname in competition_data["participants"]:
            return Response(
                {"success": False, "error": "Nickname already taken. Please choose another."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        participant_id = len(competition_data["participants"]) + 1
        competition_data["participants"][nickname] = {
            "id": participant_id,
            "is_solved": False,
            "responses": [],
        }
        set_cache_data(comp_uid, competition_data)

        return Response(
            {
                "success": True,
                "nickname": nickname,
                "participant_id": participant_id,
                "message": "Successfully joined the competition.",
            },
            status=status.HTTP_200_OK,
        )


class SubmitCodeView(APIView):
    def post(self, request):
        serializer = SubmitCodeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"success": False, "errors": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        comp_uid = serializer.validated_data.get("comp_uid")
        nickname = serializer.validated_data.get("nickname")
        user_code = serializer.validated_data.get("code")

        competition_data, error_response = get_competition_data(comp_uid)
        if error_response:
            return error_response

        if nickname not in competition_data["participants"]:
            return Response(
                {"success": False, "error": "Participant not found in this competition."},
                status=status.HTTP_404_NOT_FOUND,
            )

        task = Task.objects.get(title=competition_data["task_title"])
        results = evaluate_code(
            code=user_code, task=task, competition_uid=comp_uid, nick_name=nickname
        )
        participant_data = competition_data["participants"][nickname]

        all_passed = all(result["result"] == "pass" for result in results)
        if all_passed:
            participant_data.update(
                {
                    "is_solved": True,
                    "solved_at": timezone.now(),
                    "time_took": (timezone.now() - competition_data["created_at"]).total_seconds(),
                }
            )
            competition_data["results"].append(
                {
                    "nickname": nickname,
                    "status": "Solved",
                    "results": results,
                }
            )
            message = "All test cases passed! Task solved successfully."
        else:
            competition_data["results"].append(
                {"nickname": nickname, "status": "Failed", "results": results}
            )
            message = "Code submitted, but not all test cases passed."

        set_cache_data(comp_uid, competition_data)
        return Response(
            {"success": True, "message": message, "results": results},
            status=status.HTTP_200_OK,
        )


class StatisticsAPIView(APIView):
    def get(self, request):
        comp_uid = request.query_params.get("comp_uid")
        if not comp_uid:
            return Response(
                {"success": False, "error": "Competition UID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        competition_data, error_response = get_competition_data(comp_uid)
        if error_response:
            return error_response

        participants = competition_data.get("participants", {})
        solved_participants = [
            (nickname, p) for nickname, p in participants.items() if p.get("is_solved")
        ]
        total_participants = len(participants)
        avg_time_taken = (
            sum(p.get("time_took", 0) for p in participants.values()) / total_participants
            if total_participants
            else 0
        )

        winner = (
            min(
                solved_participants,
                key=lambda x: x[1].get("time_took", float("inf")),
            )
            if solved_participants
            else None
        )
        winner_data = (
            {"nickname": winner[0], "time_took": round(winner[1].get("time_took"), 2)}
            if winner
            else None
        )

        statistics = {
            "total_participants": total_participants,
            "solved_count": len(solved_participants),
            "unsolved_count": total_participants - len(solved_participants),
            "average_time_taken": round(avg_time_taken, 2),
            "winner": winner_data,
        }
        return Response(
            {"success": True, "statistics": statistics},
            status=status.HTTP_200_OK,
        )
