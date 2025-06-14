from django.http import JsonResponse
from django.utils import timezone
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View
import json 
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from celery import shared_task
from datetime import date
from asgiref.sync import sync_to_async

from apps.competition.utils.random_task import get_random
from apps.competition.utils.generators import generator_uid
from apps.competition.utils.evaluate_code import evaluate_code
from apps.competition.utils.generate_function_name import generate_function_name

import asyncio
from apps.competition.models import CompetitionStatisticsModel
from .serializers import (
    CompetitionJoinSerializer,
    CompetitionValidateSerializer,
    SubmitCodeSerializer,
)
from apps.task.models import Task

def get_task_by_name_sync():
    """
    Synchronous function to get a Task by its name.
    This assumes that the task exists.
    """
    return Task.objects.get(title="Last Stone Weight")

# Wrap the synchronous function with sync_to_async
get_task_by_name = sync_to_async(get_task_by_name_sync)
# Declare default data about today's comeptitions
@shared_task() 
def create_daily_statistics():
    today = date.today()
    if not CompetitionStatisticsModel.objects.filter(date=today).exists():
        CompetitionStatisticsModel.objects.create()

# Utility functions for common operations
def get_competition_data(comp_uid):
    competition_data = cache.get(comp_uid)
    if not competition_data:
        return None, Response(
            {"success": False, "error": "Competition not found or expired."},
            status=status.HTTP_404_NOT_FOUND,
        )
    return competition_data, None

# Declarating every competition to today's statistics
def declare_comeptition_to_statistics(task):
    today = date.today()
    statistics, created = CompetitionStatisticsModel.objects.get_or_create(date=today)
    statistics.total_competitions += 1
    # statistics.tasks.add(task)
    statistics.save()


async def set_cache_data(comp_uid, competition_data):
    duration = (competition_data.get("duration", 0) + 5) * 60  # Convert to seconds
    cache.set(comp_uid, competition_data, timeout=duration)

@method_decorator(csrf_exempt, name='dispatch')
class CompetitionAPIView(View):
    async def get(self, request):
        today = date.today()

        # Fetch or create statistics for today
        statistics_today, _ = await asyncio.to_thread(
            CompetitionStatisticsModel.objects.get_or_create, date=today
        )

        # Fetch all statistics asynchronously
        statistics_all = await asyncio.to_thread(
            list, CompetitionStatisticsModel.objects.all()
        )

        # Prepare statistics for all time
        statistics = {
            str(stat.date): {
                "total_competitions": stat.total_competitions
            }
            for stat in statistics_all
        }

        # Prepare response data
        data = {
            "today": {
                "date": statistics_today.date,
                "total_competitions": statistics_today.total_competitions,
            },
            "all_time": statistics,
        }

        return JsonResponse(data, status=200)

    async def post(self, request):
        try:
            body = json.loads(request.body)  # Parse JSON body
        except json.JSONDecodeError:
            return JsonResponse(
                {"success": False, "message": "Invalid JSON."},
                status=400,
            )

        serializer = CompetitionValidateSerializer(data=body)
        if not serializer.is_valid():
            return JsonResponse(
                {"success": False, "errors": serializer.errors},
                status=400,
            )
        
           
        # difficulty = serializer.validated_data.get("difficulty")
        task_coro = get_task_by_name()
        # random_task_coro = asyncio.to_thread(get_random, difficulty=difficulty)
        uid_generation_coro = asyncio.to_thread(generator_uid)

        task, comp_uid = await asyncio.gather(task_coro, uid_generation_coro)

        if not task:
            return JsonResponse(
                {"success": False, "message": "No task available for the specified difficulty."},
                status=404,
            )

        if cache.get(comp_uid):
            return JsonResponse(
                {"success": False, "message": "Please regenerate again!"},
                status=400,
            )

        function_name = generate_function_name(task)
        comp_data = {
            "competition_uid": comp_uid,
            **serializer.validated_data,
            "task_title": task.title,
            "function_name": function_name,
            "is_started": False,
            "participants": {},
            "created_at": timezone.now(),
            "results": [],
        }

        cache_task = asyncio.create_task(set_cache_data(comp_uid, comp_data))
        task_data = await asyncio.to_thread(self._prepare_task_data, task)

        await cache_task

        await asyncio.to_thread(declare_comeptition_to_statistics, task)

        return JsonResponse(
            {
                "success": True,
                "competition_uid": comp_uid,
                "task": task_data,
                "function_name": function_name,
                "message": "Competition created successfully.",
            },
            status=201,
        )


    def _prepare_task_data(self, task):
        """
        Synchronous helper method to prepare task data.
        """
        return {
            "id": task.id,
            "title": task.title,
            "difficulty": task.difficulty,
            "description": task.description,
            "test_cases": list(task.test_cases.all().values(
                "input", "output", "input_type", "output_type"
            )),
        }
        
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
