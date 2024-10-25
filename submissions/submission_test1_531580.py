def plus_one(digits):
    n = len(digits)
    for i in range(n - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] 

if __name__ == "__main__":
    import sys, json
    data = json.loads(sys.stdin.read())
    result = plus_one(**data)
    print(result)
