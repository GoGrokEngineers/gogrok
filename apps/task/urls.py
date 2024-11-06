from django.urls import path
from .views import TaskListView, TaskDetailView, TaskTestCaseDeleteView

urlpatterns = [
    path('tasks/', TaskListView.as_view(), name='task_list'),
    path('task/<int:id>/', TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:id>/testcases/delete/', TaskTestCaseDeleteView.as_view(), name='task-testcase-delete'),
]
