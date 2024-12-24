from django.db import models

class CompetitionStatisticsModel(models.Model):
    date = models.DateField(auto_now=True)
    # tasks = models.ManyToManyField("task.Task")
    total_competitions = models.IntegerField(default=0)
