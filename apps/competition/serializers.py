from rest_framework import serializers

DIFFICULTY_CHOICES = {"Easy": "Easy", "Medium": "Medium", "Hard": "Hard"}
DURATION_CHOICES = {30: 30, 40: 40, 60: 60, 90: 90}


class CompetitionValidateSerializer(serializers.Serializer):
    """
    Serializer to validate competition data.
    """
    comp_uid = serializers.CharField(read_only=True)
    difficulty = serializers.ChoiceField(choices=DIFFICULTY_CHOICES)
    duration = serializers.ChoiceField(choices=DURATION_CHOICES)
    participants = serializers.DictField()
    results = serializers.ListField(read_only=True)

    def create(self, validated_data):
        """
        Placeholder for create functionality if needed in the future.
        """
        return validated_data

    def update(self, instance, validated_data):
        """
        Placeholder for update functionality if needed in the future.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance


class CompetitionJoinSerializer(serializers.Serializer):
    """
    Serializer to join a competition.
    """
    comp_uid = serializers.CharField(max_length=50)
    nickname = serializers.CharField(max_length=25)

    def create(self, validated_data):
        """
        Placeholder for create functionality if needed in the future.
        """
        return validated_data

    def update(self, instance, validated_data):
        """
        Placeholder for update functionality if needed in the future.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance


class SubmitCodeSerializer(serializers.Serializer):
    """
    Serializer to submit code for a competition.
    """
    comp_uid = serializers.CharField(max_length=50)
    nickname = serializers.CharField(max_length=25)
    code = serializers.JSONField()

    def create(self, validated_data):
        """
        Placeholder for create functionality if needed in the future.
        """
        return validated_data

    def update(self, instance, validated_data):
        """
        Placeholder for update functionality if needed in the future.
        """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        return instance
