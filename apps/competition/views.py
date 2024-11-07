from django.utils import timezone
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.competition.utils.random_task import get_random
from apps.competition.utils.generators import generator_uid
from .serializers import CompetionJoinSerializer, CompetitionValidateSerializer

competitions_list = []
class CompetitionCreateView(APIView):

    def get(self, request):
    
        competition_keys = cache.keys('*')

        competitions_data = []
        
        for comp_uid in competition_keys:
            competition = cache.get(comp_uid)
            if competition:
                competitions_data.append(competition)

        # Serialize all competitions data
        serialized_data = CompetitionValidateSerializer(competitions_data, many=True).data

        return Response({
            "success": True,
            "competitions": serialized_data,
            "message": "Competitions retrieved successfully."
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CompetitionValidateSerializer(data=request.data)
        if serializer.is_valid():
            difficulty = serializer.validated_data.get("difficulty")
            task = get_random(difficulty)

            if not task:
                return Response({"success": False, "message": "No task available for the specified difficulty."}, 
                                status=status.HTTP_404_NOT_FOUND)
            

            comp_uid = generator_uid()
            if cache.get(comp_uid):
                return Response({"success": False, "message": "Please regenerate again!"}, 
                                status=status.HTTP_400_BAD_REQUEST)

            comp_data = {
                "competition_uid": comp_uid,
                **serializer.validated_data,
                "task_id": task.title,  
                "created_at": timezone.now(),
                "results": [],
            }

            # Store the competition data in Redis cache
            cache.set(comp_uid, comp_data, timeout=comp_data["duration"] * 60)
            competitions_list.append(comp_data)

            return Response({
                "success": True,
                "competition_uid": comp_uid,
                "task": {"id" : task.id, "title": task.title, "difficulty": task.difficulty, "description" : task.description, "task_testcases" : task.test_cases.all().values("input", "output", "input_type", "output_type")}, # "task_testcases" : task.test_cases()
                "message": "Competition created successfully."
            }, status=status.HTTP_201_CREATED)

        
        return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class JoinCompetitionView(APIView):
    def post(self, request):
        
        serializer = CompetionJoinSerializer(data=request.data)
        
       
        if not serializer.is_valid():
            return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        
        comp_uid = serializer.validated_data.get("comp_uid")
        nickname = serializer.validated_data.get("nickname")

        competition_data = cache.get(comp_uid)
        if not competition_data:
            return Response({"success": False, "error": "Competition not found or expired."}, status=status.HTTP_404_NOT_FOUND)
       
        if nickname in competition_data["participants"]:
            return Response({"success": False, "error": "Nickname already taken. Please choose another."}, status=status.HTTP_400_BAD_REQUEST)


        participant_id = len(competition_data["participants"]) + 1
        competition_data["participants"][nickname] = {
            "id": participant_id,
            'is_solved': False,
            # Future feature placeholders (commented out if not used)
            'time_took': 0,
            'score': 0,
            'responses': []
        }

        
        cache.set(comp_uid, competition_data, timeout=competition_data.get("duration", 0) * 60)  # Duration in seconds

        # Print competition data for debugging
        print(f"Competition Data: {competition_data}, Type: {type(competition_data)}")

      
        return Response({
            "success": True,
            "nickname": nickname,
            "participant_id": participant_id,
            "message": "Successfully joined the competition."
        }, status=status.HTTP_200_OK)        


class StatisticsAPIVIew(APIVIew):
    def get(self, request):
        comp_uid = request.data.get('comp_uid')
        competition_data = cache.get(comp_uid)
        if not competition_data:
            return Response({"success": False, "error": "Competition not found or expired."}, status=status.HTTP_404_NOT_FOUND)
       
        statistics = {}
        return Response({
            "success": True,
            "statistics": statistics
            
        }, status=status.HTTP_200_OK)      