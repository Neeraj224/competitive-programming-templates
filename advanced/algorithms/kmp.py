def build_lps(pattern):
    # LPS (Longest Prefix Suffix) array
    #
    # lps[i] = length of longest prefix of pattern
    #          which is also a suffix ending at index i
    #
    # this tells us:
    # if mismatch happens at i,
    # where to resume in the pattern without rechecking everything

    lps = [0] * len(pattern)

    # j tracks length of current matching prefix
    j = 0

    for i in range(1, len(pattern)):
        # if mismatch, fallback to shorter prefix using lps
        # this avoids restarting from scratch
        while j > 0 and pattern[i] != pattern[j]:
            j = lps[j - 1]

        # if characters match, extend current prefix
        if pattern[i] == pattern[j]:
            j += 1
            lps[i] = j

    return lps


def kmp_search(text, pattern):
    # KMP avoids rechecking characters in text
    #
    # when mismatch happens,
    # use LPS to decide next comparison
    #
    # guarantees linear time O(n + m)

    lps = build_lps(pattern)

    j = 0
    result = []

    for i in range(len(text)):
        # fallback using LPS instead of restarting match
        while j > 0 and text[i] != pattern[j]:
            j = lps[j - 1]

        # match current character
        if text[i] == pattern[j]:
            j += 1

        # full pattern matched
        if j == len(pattern):
            result.append(i - j + 1)

            # continue searching for next match
            j = lps[j - 1]

    return result


def main():
    text = "ababcababcabc"
    pattern = "ababc"

    print(kmp_search(text, pattern))


if __name__ == "__main__":
    main()