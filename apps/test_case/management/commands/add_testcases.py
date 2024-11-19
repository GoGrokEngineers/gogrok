from django.core.management.base import BaseCommand
from apps.task.models import Task
from apps.test_case.models import TestCase

class Command(BaseCommand):
    help = 'Add test cases to each specific task'

    def handle(self, *args, **options):

        test_cases = [
    {
			"input": {
				"prices": [
					7,
					1,
					5,
					3,
					6,
					4
				]
			},
			"output": 5,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					7,
					6,
					4,
					3,
					1
				]
			},
			"output": 0,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					1,
					2,
					3,
					4,
					5,
					6,
					7,
					8,
					9
				]
			},
			"output": 8,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					9,
					8,
					7,
					6,
					5,
					4,
					3,
					2,
					1
				]
			},
			"output": 0,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					2,
					4,
					1
				]
			},
			"output": 2,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					1,
					2,
					4,
					2,
					5,
					7,
					2,
					4,
					9,
					0
				]
			},
			"output": 8,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					3,
					3,
					5,
					0,
					0,
					3,
					1,
					4
				]
			},
			"output": 4,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					7,
					2,
					5,
					3,
					6,
					1,
					4
				]
			},
			"output": 4,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					7,
					1,
					5,
					3,
					6,
					4,
					8
				]
			},
			"output": 7,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					1,
					3,
					2,
					8,
					4,
					9
				]
			},
			"output": 8,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					5,
					4,
					3,
					2,
					1,
					10
				]
			},
			"output": 9,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					8,
					1,
					2,
					4,
					6,
					3,
					9
				]
			},
			"output": 8,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					3,
					6,
					1,
					3,
					4,
					8,
					2,
					9
				]
			},
			"output": 8,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					1,
					9,
					6,
					4,
					3,
					1,
					8
				]
			},
			"output": 8,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		},
		{
			"input": {
				"prices": [
					1,
					6,
					7,
					9,
					5,
					3,
					8
				]
			},
			"output": 8,
			"input_type": {
				"prices": "List[int]"
			},
			"output_type": {
				"result": "int"
			}
		}



]
        

        task = Task.objects.get(title="Best Time to Buy and Sell Stock")

        for test_case_data in test_cases:
            TestCase.objects.get_or_create(
                task=task,
                input=test_case_data["input"],
                output=test_case_data["output"],
                input_type=test_case_data["input_type"],
                output_type=test_case_data["output_type"]
            )