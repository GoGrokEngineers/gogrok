def two_sum(nums, target):
    num_map = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_map:
            return [num_map[complement], i]
        num_map[num]

if __name__ == "__main__":
    import sys, json
    data = json.loads(sys.stdin.read())
    result = two_sum(**data)
    print(result)
