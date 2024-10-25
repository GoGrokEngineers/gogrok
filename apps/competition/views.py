import time
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from apps.competition.utils import generators
from serializers import CompetionJoinSerializer


class CompetitionCreateView(APIView):
    def post(self, request):
        DIFFICULTY_CHOICES = {"Easy": "Easy", "Medium": "Medium", "Hard": "Hard"}
        DURATION_CHOICES = {30: 30, 40: 40, 60: 60, 90: 90} 

        try:
            # Serialize it -> eng2neer(Feruzbek)
            difficulty = DIFFICULTY_CHOICES[request.data.get("difficulty")]
            duration = DURATION_CHOICES[request.data.get("duration")]
            capacity = request.data.get("duration")

            competition_uid = generators.generator_uid()

            competition_data = {
                "participants": {},
                "results": [],
                "difficulty": difficulty,
                "duration": duration,
                "capacity": capacity,
                "created_at": time.time(),
            }

            cache.set(competition_uid, competition_data, timeout=duration*60)

            return Response({
                "success": True,
                "competition_uid": competition_uid,
                "message": "Competition created successfully."
            }, status=status.HTTP_201_CREATED)

        except KeyError as ex:
            return Response({"success": False, "error": f"Invalid value: {str(ex)}"}, status=status.HTTP_400_BAD_REQUEST)


class JoinCompetitionView(APIView):
    def post(self, request):
       
        serializer = CompetionJoinSerializer(request.data)

        comp_uid = request.data.get("comp_uid")
        nickname = request.data.get("nickname")
        competition_data = cache.get(comp_uid)
        if not competition_data:
            return Response({"success": False, "error": "Competition not found or expired."}, status=status.HTTP_404_NOT_FOUND)

        if nickname in competition_data["participants"]:
            return Response({"success": False, "error": "Nickname already taken. Please choose another."}, status=status.HTTP_400_BAD_REQUEST)

        participant_id = len(competition_data["participants"]) + 1 
        competition_data["participants"][nickname] = {
            "id": participant_id,
            'did_solve': False,
            #Future features
            'time_took': 0,
            "score": 0,
            "responses": []
        }

        cache.set(comp_uid, competition_data, timeout=competition_data["duration"])

        return Response({
            "success": True,
            "nickname": nickname,
            "participant_id": participant_id,
            "message": "Successfully joined the competition."
        }, status=status.HTTP_200_OK)      