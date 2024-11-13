from django.core.management.base import BaseCommand
from apps.task.models import Task
from apps.test_case.models import TestCase

class Command(BaseCommand):
    help = 'Add test cases to each specific task'

    def handle(self, *args, **options):

        test_cases = [
    {
        "input": {"nums": [2, 7, 11, 15], "target": 9},
        "output": [0, 1],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [3, 2, 4], "target": 6},
        "output": [1, 2],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [3, 3], "target": 6},
        "output": [0, 1],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [1, 2, 3, 4, 5], "target": 9},
        "output": [3, 4],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [5, 5, 11, 3], "target": 10},
        "output": [0, 1],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [0, 4, 3, 0], "target": 0},
        "output": [0, 3],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [-3, 4, 3, 90], "target": 0},
        "output": [0, 2],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [1, 5, 3, 7, 2, 8], "target": 10},
        "output": [2, 3],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [3, 5, 7, 8, 4, 2], "target": 9},
        "output": [1, 4],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [1, 2, 3, 4, 5, 6, 7], "target": 13},
        "output": [5, 6],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [10, 20, 10, 40, 50, 30, 70], "target": 110},
        "output": [3, 6],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [1, 1, 1, 1, 1, 1], "target": 2},
        "output": [0, 1],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [-1, -2, -3, -4, -5], "target": -8},
        "output": [2, 4],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [2, 5, 5, 11, 1], "target": 10},
        "output": [1, 2],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    },
    {
        "input": {"nums": [1, 3, 3, 6, 10], "target": 9},
        "output": [2, 3],
        "input_type": {"nums": "list[int]", "target": "int"},
        "output_type": {"result": "list[int]"}
    }




]
        

        task = Task.objects.get(title="Two Sum")

        for test_case_data in test_cases:
            TestCase.objects.get_or_create(
                task=task,
                input=test_case_data["input"],
                output=test_case_data["output"],
                input_type=test_case_data["input_type"],
                output_type=test_case_data["output_type"]
            )