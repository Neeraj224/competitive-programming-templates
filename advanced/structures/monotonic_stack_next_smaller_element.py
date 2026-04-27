def next_smaller_element(nums):
    # maintain increasing stack
    #
    # when current element is smaller,
    # it becomes the "next smaller" for previous elements

    n = len(nums)
    result = [-1] * n

    stack = []

    for i in range(n):
        while stack and nums[i] < nums[stack[-1]]:
            idx = stack.pop()
            result[idx] = nums[i]

        stack.append(i)

    return result


def main():
    nums = [4, 8, 5, 2, 25]
    print(next_smaller_element(nums))


if __name__ == "__main__":
    main()