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
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [3, 2, 4], "target": 6},
        "output": [1, 2],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [3, 3], "target": 6},
        "output": [0, 1],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [1, 5, 3, 7, 2, 8], "target": 10},
        "output": [3, 5],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [0, 4, 3, 0], "target": 0},
        "output": [0, 3],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [-1, -2, -3, -4, -5], "target": -8},
        "output": [2, 4],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [1, 2, 3, 4, 5], "target": 6},
        "output": [0, 4],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [100000, 99999, -1, 1], "target": 99998},
        "output": [1, 2],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [10, 15, -15, -10, 0], "target": 0},
        "output": [0, 3],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [8, 2, 6, 4, 7, 3], "target": 9},
        "output": [1, 5],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [-10, 7, 19, 21, 5, -7], "target": 12},
        "output": [1, 2],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [1, 1, 1, 2, 2, 3], "target": 4},
        "output": [3, 5],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [2, 4, 6, 8, 10, 12], "target": 16},
        "output": [3, 4],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [3, 5, -4, 8, 11, 1, -1, 6], "target": 10},
        "output": [1, 6],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
    },
    {
        "input": {"nums": [4, 5, 1, -3, -5, 9, 7, 2], "target": 0},
        "output": [1, 4],
        "input_type": {"nums": "list", "target": "int"},
        "output_type": {"result": "list"}
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