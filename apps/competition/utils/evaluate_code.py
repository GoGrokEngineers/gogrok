import subprocess
import os
import json
from .generate_function_name import generate_function_name
from django.conf import settings

is_root = False
def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def build_tree(data):
    if not data:
        return None
    root = TreeNode(data['val'])
    if 'left' in data:
        root.left = build_tree(data['left'])
    if 'right' in data:
        root.right = build_tree(data['right'])
    return root


def evaluate_code(code : str, task, competition_uid, nick_name):
    function_name = generate_function_name(task)
    print(function_name)
    folder = "submissions"
    results = []

    file_name = os.path.join(settings.BASE_DIR, folder, f"submission_{nick_name}_{competition_uid}.py")
    wrapper_code = f"""
if __name__ == "__main__":
    import sys, json
    data = json.loads(sys.stdin.read())
    result = {function_name}(**data)  
    print(result)
    """
    test_cases = task.test_cases.all()  
        
    requires_tree = any('root' in test_case.input for test_case in test_cases)

    # Generate wrapper code
    if requires_tree:
        wrapper_code = f"""
if __name__ == "__main__":
    import sys, json

    class TreeNode:
        def __init__(self, val=0, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

    def build_tree(data):
        if data is None:
            return None
        node = TreeNode(data['val'])
        if 'left' in data:
            node.left = build_tree(data['left'])
        if 'right' in data:
            node.right = build_tree(data['right'])
        return node

    data = json.loads(sys.stdin.read())
    if 'root' in data:
        data['root'] = build_tree(data['root'])

    result = {function_name}(**data)
    print(result)
"""
    else:
        wrapper_code = f"""
if __name__ == "__main__":
    import sys, json
    data = json.loads(sys.stdin.read())
    result = {function_name}(**data)
    print(result)
"""
         
    try:
       
        with open(file_name, "w") as f:
            f.write(code)
            f.write("\n")
            f.write(wrapper_code)
    
        # Prepare results for each test case associated with the task
        test_cases = task.test_cases.all()  
        
        for i, test_case in enumerate(test_cases):
            # Convert the input data to JSON
            input_data = json.dumps(test_case.input)
            print(input_data)
           
            try:
                result = subprocess.run(
                    ['python3', file_name],
                    input=input_data,  
                    text=True,
                    capture_output=True,
                    timeout=5  
                )
                print(result)
                
                
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
                       
                else:
                    results.append({
                        "test_case": i + 1,
                        "result": "error",
                        "error": result.stderr.strip()
                    })
                    

            except subprocess.TimeoutExpired:
                results.append({
                    "test_case": i + 1,
                    "result": "error",
                    "error": "Execution timed out."
                })

    finally:
        all_passed = all(result['result'] == 'pass' for result in results)
        delete_file(file_name)

    return results
