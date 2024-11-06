import os
import django
import unittest

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # replace 'your_project' with your project name
django.setup()

from django.test import TestCase
from apps.task.models import Task
from apps.competition.utils.evaluate_code import evaluate_code

class CompetitionEvaluationTest(TestCase):
    def setUp(self):
        # Assuming self.task is already populated with test cases in the database.
        self.task = Task.objects.get(title="Two Sum")  # Retrieve an existing task with test cases.

    def test_evaluate_code(self):
        # Mock user code that we expect to match the test cases
        user_code = """
def two_sum(nums, target):
    lookup = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in lookup:
            return [lookup[complement], i]
        lookup[num] = i
    return []

if __name__ == "__main__":
    import sys, json
    data = json.loads(sys.stdin.read())
    result = two_sum(data['nums'], data['target'])
    print(result)
    """
        
        # Evaluate the user's code with the task's test cases
        results = evaluate_code(user_code, self.task, competition_uid="test_uid", nick_name="test_user")
        for i, result in enumerate(results):
            if result['result'] == "pass":
                print(f"Test Case {i + 1}: Passed - Output: {result['output']}")
            elif result['result'] == "fail":
                print(f"Test Case {i + 1}: Failed - Output: {result['output']} - Expected: {result['expected']}")
            elif result['result'] == "error":
                print(f"Test Case {i + 1}: Error - Error Message: {result['error']}")
       
        self.assertTrue(all(result['result'] == "pass" for result in results))
# To run the test
if __name__ == "__main__":
    unittest.main()
