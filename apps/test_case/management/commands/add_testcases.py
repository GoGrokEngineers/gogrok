from django.core.management.base import BaseCommand
from apps.task.models import Task
from apps.test_case.models import TestCase

class Command(BaseCommand):
    help = 'Add test cases to each specific task'

    def handle(self, *args, **options):

        test_cases = [
    {
    "input": { "nums1": [1, 2, 3, 0, 0, 0], "m": 3, "nums2": [2, 5, 6], "n": 3 },
    "output": [1, 2, 2, 3, 5, 6],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [1], "m": 1, "nums2": [], "n": 0 },
    "output": [1],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [0], "m": 0, "nums2": [1], "n": 1 },
    "output": [1],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [2, 0], "m": 1, "nums2": [1], "n": 1 },
    "output": [1, 2],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [4, 5, 6, 0, 0, 0], "m": 3, "nums2": [1, 2, 3], "n": 3 },
    "output": [1, 2, 3, 4, 5, 6],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [1, 3, 5, 0, 0, 0], "m": 3, "nums2": [2, 4, 6], "n": 3 },
    "output": [1, 2, 3, 4, 5, 6],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [0, 0, 0, 0, 0], "m": 0, "nums2": [1, 2, 3, 4, 5], "n": 5 },
    "output": [1, 2, 3, 4, 5],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [1, 2, 0, 0], "m": 2, "nums2": [3, 4], "n": 2 },
    "output": [1, 2, 3, 4],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [0, 0, 0, 0, 0], "m": 0, "nums2": [0, 0, 0, 0, 0], "n": 5 },
    "output": [0, 0, 0, 0, 0],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [1, 2, 3, 0, 0, 0], "m": 3, "nums2": [-1, -2, -3], "n": 3 },
    "output": [-3, -2, -1, 1, 2, 3],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [-5, -4, 0, 0, 0, 0], "m": 2, "nums2": [-3, -2, -1, 0], "n": 4 },
    "output": [-5, -4, -3, -2, -1, 0],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [4, 0, 0, 0, 0, 0], "m": 1, "nums2": [1, 2, 3, 5, 6], "n": 5 },
    "output": [1, 2, 3, 4, 5, 6],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [3, 0, 0, 0], "m": 1, "nums2": [1, 2, 4], "n": 3 },
    "output": [1, 2, 3, 4],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [2, 4, 6, 0, 0, 0], "m": 3, "nums2": [1, 3, 5], "n": 3 },
    "output": [1, 2, 3, 4, 5, 6],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
},
{
    "input": { "nums1": [1, 3, 5, 7, 0, 0, 0], "m": 4, "nums2": [2, 4, 6], "n": 3 },
    "output": [1, 2, 3, 4, 5, 6, 7],
    "input_type": { "nums1": "List[int]", "m": "int", "nums2": "List[int]", "n": "int" },
    "output_type": { "result": "List[int]" }
}





]
        

        task = Task.objects.get(title="Merge Sorted Array")

        for test_case_data in test_cases:
            TestCase.objects.get_or_create(
                task=task,
                input=test_case_data["input"],
                output=test_case_data["output"],
                input_type=test_case_data["input_type"],
                output_type=test_case_data["output_type"]
            )