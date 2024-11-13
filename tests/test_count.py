# In order to know count of the testcases of each task

import os
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Replace 'yourproject' with your project name

# Setup Django
django.setup()
from apps.task.models import Task
# Replace 'task_id' with the ID of the task you want to check
tasks = Task.objects.all()

for task in tasks:
    testcase_count = task.test_cases.count()
    if testcase_count == 15:
        print(f'Task ID {task.id} has exactly 15 test cases.')
    else:
        print(f'Task ID {task.id} has {testcase_count} test cases.')

