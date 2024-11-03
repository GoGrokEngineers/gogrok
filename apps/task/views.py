from django.shortcuts import render
from .serializers import TaskSerializer, Task
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
# Create your views here.


class TaskListView(generics.ListAPIView):
    queryset = Task.objects.prefetch_related('test_cases').all()
    serializer_class = TaskSerializer

# Retrieve a single task with its test cases
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.prefetch_related('test_cases').all()
    serializer_class = TaskSerializer
    lookup_field = 'id'


class TaskTestCaseDeleteView(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        test_cases_count = task.test_cases.count()
        
        # Delete all related test cases
        task.test_cases.all().delete()
        
        return Response(
            {
                "message": f"Deleted {test_cases_count} test case(s) associated with task '{task.title}'."
            },
            status=status.HTTP_204_NO_CONTENT
        )