class TrieNode:
    def __init__(self):
        # each node branches on characters
        self.children = {}

        # marks end of a valid word
        self.is_end = False


class Trie:
    def __init__(self):
        # root represents empty prefix
        self.root = TrieNode()

    def insert(self, word):
        # walk through characters, creating nodes as needed

        node = self.root

        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()

            node = node.children[ch]

        node.is_end = True

    def search(self, word):
        # check if full word exists

        node = self._find(word)
        return node is not None and node.is_end

    def startsWith(self, prefix):
        # check if prefix path exists

        return self._find(prefix) is not None

    def _find(self, s):
        # helper to traverse trie

        node = self.root

        for ch in s:
            if ch not in node.children:
                return None

            node = node.children[ch]

        return node


def main():
    trie = Trie()

    trie.insert("apple")

    print(trie.search("apple"))
    print(trie.search("app"))
    print(trie.startsWith("app"))


if __name__ == "__main__":
    main()
