from rest_framework import serializers
from .models import Task
from apps.test_case.models import TestCase
class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestCase
        fields = ['input', 'output', 'input_type', 'output_type']

class TaskSerializer(serializers.ModelSerializer):
    test_cases = TestCaseSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'difficulty', "test_cases"]