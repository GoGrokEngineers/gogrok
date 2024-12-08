from django.core.management.base import BaseCommand
from apps.task.models import Task
from apps.test_case.models import TestCase

class Command(BaseCommand):
    help = 'Add test cases to each specific task'

    def handle(self, *args, **options):

        test_cases = [
            {
            "input": {
                "nums": [3, 2, 3]
            },
            "output": 3,
            "input_type": {
                "nums": "list[int]"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "nums": [2, 2, 1, 1, 1, 2, 2]
            },
            "output": 2,
            "input_type": {
                "nums": "list[int]"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "nums": [1]
            },
            "output": 1,
            "input_type": {
                "nums": "list[int]"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "nums": [1, 1, 2]
            },
            "output": 1,
            "input_type": {
                "nums": "list[int]"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "nums": [5, 5, 5, 2, 3, 5, 5]
            },
            "output": 5,
            "input_type": {
                "nums": "list[int]"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "nums": [8, 8, 8, 1, 2, 3, 8, 8, 8]
            },
            "output": 8,
            "input_type": {
                "nums": "list[int]"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "nums": [10, 10, 10, 10, 1, 2, 3]
            },
            "output": 10,
            "input_type": {
                "nums": "list[int]"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "nums": [9, 9, 9, 9, 9, 3, 3, 3]
            },
            "output": 9,
            "input_type": {
                "nums": "list[int]"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "nums": [6, 6, 6, 7, 7, 7, 7]
            },
            "output": 7,
            "input_type": {
                "nums": "list[int]"
            },
            "output_type": {
                "result": "int"
            }
        },
        {
            "input": {
                "nums": [1, 2, 3, 2, 2, 2, 2]
            },
            "output": 2,
            "input_type": {
                "nums": "list[int]"
            },
            "output_type": {
                "result": "int"
            }
        }
		]
        

        task = Task.objects.get(title="Majority Element")

        for test_case_data in test_cases:
            TestCase.objects.get_or_create(
                task=task,
                input=test_case_data["input"],
                output=test_case_data["output"],
                input_type=test_case_data["input_type"],
                output_type=test_case_data["output_type"]
            )