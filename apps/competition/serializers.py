from rest_framework import serializers


DIFFICULTY_CHOICES = {"Easy": "Easy", "Medium": "Medium", "Hard": "Hard"}
DURATION_CHOICES = {30: 30, 40: 40, 60: 60, 90: 90} 


class CompetitionValidateSerializer(serializers.Serializer):
    comp_uid = serializers.CharField(read_only=True)
    difficulty = serializers.ChoiceField(choices=DIFFICULTY_CHOICES)
    duration = serializers.ChoiceField(choices=DURATION_CHOICES)
    participants = serializers.DictField()
    results = serializers.ListField(read_only=True)

class CompetionJoinSerializer(serializers.Serializer):
    comp_uid = serializers.CharField(max_length=50)
    nickname = serializers.CharField(max_length=25)



class SumbitCodeSerializer(serializers.Serializer):
    comp_uid = serializers.CharField(max_length=50)
    nickname = serializers.CharField(max_length=25)
    code = serializers.JSONField()