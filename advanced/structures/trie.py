class TrieNode:
    def __init__(self):
        # any trie node can have children - but instead of doing an array
        # over here, we will do a hashmap, coz thats easier and faster
        self.children = {}
        # we can mark nodes as if they represent the end of a single 
        # word in our Trie, so we need a flag to represent that
        self.end_of_word = False
        
        # note: we are not storing the character itself in the TrieNode here
        # it's gonna be implicit from the children hashmap that we have
        # so lets say if we were adding a lowercase character a, we would do:
        # children['a'] = TrieNode() -> a is the key and we are creating a 
        # TrieNode for that character - no need to complicate it further

class Trie:
    def __init__(self):
        # for the constructor for our Trie/Prefix tree we will simply
        # initialize a root node, and nothing else:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        """
            insert the word in our Trie/Prefix Tree
        """
        # now for insert we will have to iterate through every character in 
        # the word that we are given for insertion:
        # initially the current is gonna be set to the root - we will start with it
        current = self.root
        
        # and while going throuhg the characters in the word, we will check first
        # if it exists or not in the current node's children (the hashmap):
        for char in word:
            # if its not in the hashmap yet
            if char not in current.children:
                # we will create a TrieNode for the character using the character
                # itself as the key for the current's hashmap:
                # basically this is how we are inserting the characters to childern
                # we are gonna use the character as a key and the value as an empty TrieNode
                # that we will later use to append more children in case words come up
                current.children[char] = TrieNode()
            # if it exists, then skip the adding part and set the current to that child
            # so that our loop continues - this way lets say if we first add 'apple'
            # we will have a node for a, p, p, l and e - but next if we try to add 'ape'
            # we woudl already have a, p - so the new e would be added as p's child:
            # existing:
            #           root
            #           /
            #          a    - > each letter is a TrieNode, and has children TrieNodes
            #         /     -> p is a's child
            #        p      the second p node
            #       / \
            #      p  e    will have e as the child for 'ape' -> here p and e are 
            #     /                                     both p's child (for apple and ape)
            #    l        and so on!
            #   /
            #  e
            
            # update current:
            current = current.children[char]

        # now by the end of our for loop, current would be set to the last character
        # of the word, so for that TrieNode, we need to set the end_of_word flag to True:
        current.end_of_word = True
        

    def search(self, word: str) -> bool:
        """
            search for the word in our Trie/Prefix Tree
        """
        # to search if a word exists or not - we need to check for the complete
        # word till we find the end_of_word flag set to True for the last character
        # becasue lets say if we have 'apple' in our Trie, then search('apple') will
        # return True, but search('app') should not!
        
        # so we will start at the root node and check if the first letter is
        # in the root's children first - if so, move to the next letter, update the
        # current and then check if the next letter is in the updated current node's children
        # and keep moving until find an end_of_word as True
        # if at any point we find that any of the letters is not in the Trie (any of the
        # node's children), then return False
        current = self.root
        
        # so, go character by character
        for char in word:
            # see if this letter exists in the children of current:
            if char not in current.children:
                # if not, return False
                return False
            
            # update current to the next child found in the Trie
            current = current.children[char]
        
        # so the above loop will iterate till the last letter of the word
        # and if we have that last letter's TrieNode in our Trie, we will return
        # it's end_of_word flag - so if that word is indeed in the Trie, it will
        # return True, otherwise, it will return False, since it would not be the end
        # of that word in the Trie
        return current.end_of_word

    def startsWith(self, prefix: str) -> bool:
        """
            check if we have any words in our Trie/Prefix Tree 
            that start with the prefix provided
        """
        # this is gonna be the exact same as the search() functionality above actually
        # but instead of returning current.end_of_word at the end, we will just return True
        # if we found the prefix of the word!
        
        # so againg we will start with the root:
        current = self.root
        
        # and go character for character in the prefix:
        for char in prefix:
            # if any of the characters in the prefix is not in any of the
            # TrieNode's children in our Trie
            if char not in current.children:
                # return False
                return False

            # update current to the next child found in the Trie for the prefix
            current = current.children[char]
        
        # and at the end if we found the part of the word (our prefix) that we were
        # searching with, we ssimply return True:
        return True
    
def main():
    # pass
    trie = Trie()
    trie.insert("apple")
    
    print(trie.search("apple"))   # return True
    print(trie.search("app"))    # return False
    print(trie.startsWith("app")) # return True
    
    trie.insert("app")
    
    print(trie.search("app"))    # return True

if __name__ == "__main__":
    main()
