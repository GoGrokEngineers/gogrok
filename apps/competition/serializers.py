from rest_framework import serializers
from .models import Competition
import random
import string
from apps.task.serializers import TaskSerializer


DIFFICULTY_CHOICES = {"Easy": "Easy", "Medium": "Medium", "Hard": "Hard"}
DURATION_CHOICES = {30: 30, 40: 40, 60: 60, 90: 90} 

class CompetionValidateSerializer(serializers.Serializer):
    difficulty = serializers.ChoiceField(choices=DIFFICULTY_CHOICES)
    

class CompetionJoinSerializer(serializers.Serializer):
    comp_uid = serializers.CharField(max_length=50)
    nick_name = serializers.CharField(max_length=25)
