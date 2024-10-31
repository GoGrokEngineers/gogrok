from django.shortcuts import render
from .serializers import TaskSerializer, Task
from rest_framework import generics
# Create your views here.


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.prefetch_related('test_cases').all()
    serializer_class = TaskSerializer

# Retrieve a single task with its test cases
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.prefetch_related('test_cases').all()
    serializer_class = TaskSerializer
    lookup_field = 'id'