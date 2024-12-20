from django.db import models
from task.models import Task

class CompetitionStatisticsModel(models.Model):
    date = models.DateField(auto_now=True)
    tasks = models.ManyToManyField(Task)
    total_competitions = models.IntegerField(default=0)
    