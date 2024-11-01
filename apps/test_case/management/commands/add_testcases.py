from django.core.management.base import BaseCommand
from apps.task.models import Task
from apps.test_case.models import TestCase

class Command(BaseCommand):
    help = 'Add test cases to each specific task'

    def handle(self, *args, **options):

        test_cases = [
    {
        "input": { "board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "word": "ABCCED" },
        "output": True,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "word": "SEE" },
        "output": True,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], "word": "ABCB" },
        "output": False,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["C","A","A"],["A","A","A"],["B","C","D"]], "word": "AAB" },
        "output": True,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A","B"],["C","D"]], "word": "AC" },
        "output": False,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A"]], "word": "A" },
        "output": True,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A","A","A","A"],["A","A","A","A"],["A","A","A","A"]], "word": "AAAAAAAAAAAAA" },
        "output": False,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A","B","C","D"],["E","F","G","H"],["I","J","K","L"]], "word": "FJ" },
        "output": False,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A","B"],["C","D"]], "word": "ABCD" },
        "output": False,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A","B","C"],["D","E","F"],["G","H","I"]], "word": "AEI" },
        "output": True,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A","B","C","D"],["E","F","G","H"],["I","J","K","L"],["M","N","O","P"]], "word": "BCGH" },
        "output": True,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A","A","A"],["A","A","A"],["A","A","A"]], "word": "AAAAA" },
        "output": True,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A","B","C"],["D","E","F"],["G","H","I"]], "word": "FG" },
        "output": False,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["C","A","A"],["A","A","A"],["B","C","D"]], "word": "CDA" },
        "output": True,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    },
    {
        "input": { "board": [["A","B","C"],["D","E","F"],["G","H","I"]], "word": "ABCDE" },
        "output": False,
        "input_type": { "board": "list[list[str]]", "word": "str" },
        "output_type": { "result": "bool" }
    }




]
        

        task = Task.objects.get(title="Word Search")

        for test_case_data in test_cases:
            TestCase.objects.get_or_create(
                task=task,
                input=test_case_data["input"],
                output=test_case_data["output"],
                input_type=test_case_data["input_type"],
                output_type=test_case_data["output_type"]
            )