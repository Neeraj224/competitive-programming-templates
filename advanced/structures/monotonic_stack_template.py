def monotonic_stack_template(nums):
    # this is the core pattern
    #
    # change the comparison based on problem:
    # >  => next greater
    # <  => next smaller
    #
    # reverse traversal => previous greater/smaller

    stack = []
    result = [-1] * len(nums)

    for i in range(len(nums)):
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]

        stack.append(i)

    return result