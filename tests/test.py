import sys
import json

def square_elements(arr):
    for i in range(len(arr)):
        arr[i] = arr[i] * arr[i]
    return arr

if __name__ == "__main__":
    input_data = json.loads(sys.argv[1])  # Parse the input JSON
    result = square_elements(input_data)
    print(json.dumps(result))  # Output as JSON string
