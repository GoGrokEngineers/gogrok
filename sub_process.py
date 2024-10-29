import subprocess
import json

def evaluate_code():
    results = []
    test_cases = [
        {"input": [10, 5], "expected_output": [100, 25]},
        {"input": [5, 6], "expected_output": [25, 37]}  # Corrected expected output
    ]

    file_name = "test.py"  # Assumes test.py with square_elements function is already present

    for i, test_case in enumerate(test_cases):
        # Run test.py and pass input as a JSON string argument
        result = subprocess.run(
            ['python3', file_name, json.dumps(test_case['input'])],  # Pass list as JSON string
            text=True,
            capture_output=True
        )

        # Parse the output back from JSON
        try:
            output = json.loads(result.stdout.strip())
            if output == test_case['expected_output']:
                results.append({"test_case": i + 1, "result": "pass", "output": output})
            else:
                results.append({"test_case": i + 1, "result": "fail", "output": output, "expected": test_case['expected_output']})
        except json.JSONDecodeError:
            results.append({"test_case": i + 1, "result": "error", "error": "Output is not valid JSON"})

    return results

print(evaluate_code())
