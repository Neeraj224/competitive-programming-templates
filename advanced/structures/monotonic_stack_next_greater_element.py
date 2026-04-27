def next_greater_element(nums):
    # Monotonic stack maintains elements in decreasing order
    #
    # idea:
    # for each element, find the next element to the right that is greater
    #
    # stack stores indices, not values
    # this allows us to map answers back to original positions
    #
    # when current element is greater than stack top,
    # it means we found "next greater" for that index

    n = len(nums)
    result = [-1] * n

    stack = []

    for i in range(n):
        # resolve all elements smaller than current
        # current element becomes their next greater
        while stack and nums[i] > nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]

        # push current index for future comparison
        stack.append(i)

    return result


def main():
    nums = [2, 1, 2, 4, 3]
    print(next_greater_element(nums))  # [4, 2, 4, -1, -1]


if __name__ == "__main__":
    main()