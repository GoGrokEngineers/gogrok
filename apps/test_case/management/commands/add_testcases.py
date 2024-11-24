from django.core.management.base import BaseCommand
from apps.task.models import Task
from apps.test_case.models import TestCase

class Command(BaseCommand):
    help = 'Add test cases to each specific task'

    def handle(self, *args, **options):

        test_cases = [
    {
			"input": {
				"nums": [
					3,
					0,
					1
				]
			},
			"output": 2,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"nums": [
					0,
					1
				]
			},
			"output": 2,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"nums": [
					9,
					6,
					4,
					2,
					3,
					5,
					7,
					0,
					1
				]
			},
			"output": 8,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"nums": [
					0
				]
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
				"nums": [
					1
				]
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
				"nums": [
					3,
					7,
					1,
					2,
					8,
					4,
					5,
					0
				]
			},
			"output": 6,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"nums": [
					45,
					35,
					44,
					30,
					40,
					33,
					36,
					43,
					41,
					32,
					31,
					29,
					42,
					38,
					37,
					34,
					46,
					39,
					47,
					48
				]
			},
			"output": 49,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"nums": [
					10000,
					0,
					9998,
					9999,
					1,
					3,
					9997,
					9996,
					9995,
					2
				]
			},
			"output": 4,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"nums": [
					0,
					3,
					4,
					2
				]
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
				"nums": [
					5,
					4,
					3,
					1,
					2,
					0,
					7,
					8,
					9
				]
			},
			"output": 6,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"nums": [
					8,
					6,
					4,
					3,
					7,
					1,
					0,
					2,
					5
				]
			},
			"output": 9,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"nums": [
					0,
					5,
					3,
					1,
					2,
					4,
					6,
					8,
					7,
					10
				]
			},
			"output": 9,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"nums": [
					0,
					2,
					3,
					1,
					5
				]
			},
			"output": 4,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"nums": [
					100000,
					99998,
					99997,
					99996,
					99999,
					100001
				]
			},
			"output": 99995,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"nums": [
					100000,
					99999,
					100001,
					100002
				]
			},
			"output": 99998,
			"input_type": {
				"nums": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		}



]
        

        task = Task.objects.get(title="Missing Number")

        for test_case_data in test_cases:
            TestCase.objects.get_or_create(
                task=task,
                input=test_case_data["input"],
                output=test_case_data["output"],
                input_type=test_case_data["input_type"],
                output_type=test_case_data["output_type"]
            )