from django.db import models
from apps.task.models import Task

class TestCase(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="test_cases")
    input = models.JSONField()
    output = models.JSONField()
    input_type = models.JSONField()
    output_type = models.JSONField()
