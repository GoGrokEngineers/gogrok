import subprocess
import os
import json

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def evaluate_code(code: str, task, competition_uid, nick_name):
    
    folder = "submissions"
    results = []
    all_passed = True


    file_name = os.path.join(folder, f"submission_{nick_name}_{competition_uid}.py")
    try:
        # Write the user's code to the temporary file
        with open(file_name, "w") as f:
            f.write(code)

        # Prepare results for each test case associated with the task
        test_cases = task.test_cases.all()  
        
        for i, test_case in enumerate(test_cases):
            # Convert the input data to JSON
            input_data = json.dumps(test_case.input)
            print(input_data)
           
            try:
                result = subprocess.run(
                    ['python', file_name],
                    input=input_data,  
                    text=True,
                    capture_output=True,
                    timeout=5  
                )
                print(result)
                
                # Check results against expected output
                if result.returncode == 0:
                    actual_output = result.stdout.strip()
                    expected_output = str(test_case.output)
                    
                    if actual_output == expected_output:
                        results.append({
                            "test_case": i + 1,
                            "result": "pass",
                            "output": actual_output
                        })
                    else:
                        results.append({
                            "test_case": i + 1,
                            "result": "fail",
                            "output": actual_output,
                            "expected": expected_output
                        })
                        all_passed = False
                else:
                    results.append({
                        "test_case": i + 1,
                        "result": "error",
                        "error": result.stderr.strip()
                    })
                    all_passed = False

            except subprocess.TimeoutExpired:
                results.append({
                    "test_case": i + 1,
                    "result": "error",
                    "error": "Execution timed out."
                })

    finally:
        if all_passed:
            delete_file(file_name)

    return results