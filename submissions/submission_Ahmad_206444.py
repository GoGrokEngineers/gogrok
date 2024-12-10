def missing_number(nums):
    n = len(nums)
    total_sum = n * (n + 1) // 2
    actual_sum = sum(nums)
    return total_sum - actual_sum

if __name__ == "__main__":
    import sys, json
    data = json.loads(sys.stdin.read())
    result = missing_number(**data)
    print(result)
