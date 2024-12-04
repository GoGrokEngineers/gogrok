def subsets(nums):
    result = [[]]  # Start with an empty subset
    for num in nums:
        result += [current + [num] for current in result]  # Add current element to all existing subsets
    return result

if __name__ == "__main__":
    import sys, json
    data = json.loads(sys.stdin.read())
    result = count_complete_tree_nodes(**data)  
    print(result)
    