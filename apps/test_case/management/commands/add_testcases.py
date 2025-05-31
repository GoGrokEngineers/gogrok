from django.core.management.base import BaseCommand
from apps.task.models import Task
from apps.test_case.models import TestCase

class Command(BaseCommand):
    help = 'Add test cases to each specific task'

    def handle(self, *args, **options):

        test_cases = [
    {
        "input": {
            "nums": [2, 7, 4, 1, 8, 1]
        },
        "output": 1,
        "input_type": {
            "nums": "List[int]"
        },
        "output_type": {
            "result": "int"
        }
    },
    {
        "input": {
            "nums": [1, 3, 2, 4, 1, 7, 8, 9, 10]
        },
        "output": 1,
        "input_type": {
            "nums": "List[int]"
        },
        "output_type": {
            "result": "int"
        }
    },
    {
        "input": {
            "nums": [10, 10, 10, 10]
        },
        "output": 0,
        "input_type": {
            "nums": "List[int]"
        },
        "output_type": {
            "result": "int"
        }
    },
    {
        "input": {
            "nums": [9, 3, 2, 10, 7, 6, 5, 1]
        },
        "output": 0,
        "input_type": {
            "nums": "List[int]"
        },
        "output_type": {
            "result": "int"
        }
    },
    {
        "input": {
            "nums": [1, 1, 1, 1, 1, 1, 1, 1]
        },
        "output": 0,
        "input_type": {
            "nums": "List[int]"
        },
        "output_type": {
            "result": "int"
        }
    },
    {
        "input": {
            "nums": [50, 49, 48, 47, 46, 45, 44, 43, 42, 41]
        },
        "output": 5,
        "input_type": {
            "nums": "List[int]"
        },
        "output_type": {
            "result": "int"
        }
    },
    {
        "input": {
            "nums": [100, 100, 99, 99, 98, 98]
        },
        "output": 0,
        "input_type": {
            "nums": "List[int]"
        },
        "output_type": {
            "result": "int"
        }
    },
    {
        "input": {
            "nums": [1, 2, 3, 100, 99, 98]
        },
        "output": 1,
        "input_type": {
            "nums": "List[int]"
        },
        "output_type": {
            "result": "int"
        }
    },
    {
        "input": {
            "nums": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        },
        "output": 5,
        "input_type": {
            "nums": "List[int]"
        },
        "output_type": {
            "result": "int"
        }
    },
    {
        "input": {
            "nums": [7, 7, 6, 6, 5, 5, 4, 4, 3, 3, 2, 2, 1, 1]
        },
        "output": 0,
        "input_type": {
            "nums": "List[int]"
        },
        "output_type": {
            "result": "int"
        }
    }
]



        

        task = Task.objects.get(title="Last Stone Weight")

        for test_case_data in test_cases:
            TestCase.objects.get_or_create(
                task=task,
                input=test_case_data["input"],
                output=test_case_data["output"],
                input_type=test_case_data["input_type"],
                output_type=test_case_data["output_type"]
            )