class Node:
    def __init__(self, leaf, frequency, letter=None):
        self.is_leaf = leaf
        self.letter = letter
        self.frequency = frequency

        self.left = None
        self.right = None


class Compression:
    def __init__(self, message):
        # Store message and welcome text
        self.uncompressed_message = message
        self.print_start()

        # Create frequency table
        self.frequency_key = {}
        self.create_frequency()

        # Start to create the tree
        self.nodes = []
        self.root_node = None
        self.create_nodes()
        self.create_tree()

        # Get a binary dictionary from the tree
        self.dictionary = {}
        self.create_dictionary(self.root_node)

        # Compress the message using dictionary and print final message
        self.compressed_message = self.compress()
        self.final_print()

    def print_start(self):
        print("Your message to compress is:\n   ", self.uncompressed_message)
        print("Uncompressed, this will take", len(self.uncompressed_message) * 7, 'bits.')

    def create_frequency(self):
        # Create a frequency table
        for letter in self.uncompressed_message:
            if letter in self.frequency_key:
                self.frequency_key[letter] += 1
            else:
                self.frequency_key[letter] = 1

        # Sort the frequencies in ascending order
        self.frequency_key = {k: v for k, v in sorted(self.frequency_key.items(), key=lambda item: item[1])}

    def create_nodes(self):
        # Create the nodes from the frequency table
        for k, v in sorted(self.frequency_key.items()):
            self.nodes.append(Node(True, v, k))

    def create_tree(self):
        # Keep collapsing until only root node
        while len(self.nodes) != 1:
            self.sort_nodes()
            left = self.nodes.pop(0)
            right = self.nodes.pop(0)
            new_node = Node(False, left.frequency+right.frequency)
            new_node.left = left
            new_node.right = right
            self.nodes.insert(0, new_node)

        # Set root node to remaining node in list
        self.root_node = self.nodes[0]

    def sort_nodes(self):
        # Sort the list of nodes in ascending depending on frequency
        self.nodes = sorted(self.nodes, key=lambda x: x.frequency)

    def create_dictionary(self, node, binary=""):
        # Create the binary dictionary recursively
        if node.is_leaf:
            self.dictionary[node.letter] = binary
        else:
            self.create_dictionary(node.left, binary+"0")
            self.create_dictionary(node.right, binary+"1")

    def compress(self):
        # Replace uncompressed message with binary
        compressed = ""
        for letter in self.uncompressed_message:
            compressed += self.dictionary[letter]

        return compressed

    def final_print(self):
        print("Your compressed message is:   ", self.compressed_message)
        print("It takes", len(self.compressed_message), "bits.")
        print("The compression ratio is: %.2f:1" % (len(self.uncompressed_message) * 7 / len(self.compressed_message)))


compressed = Compression(input("Please enter your message:\n   "))

# Save the compression data to a file
file = open("compressed-text.txt", "w+")
file.write(compressed.compressed_message + "\n")
for k, v in sorted(compressed.dictionary.items()):
    file.write(v + "," + k + "\n")