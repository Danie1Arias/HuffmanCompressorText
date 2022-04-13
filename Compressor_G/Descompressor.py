"""
Implementation of archivator using Huffman coding
works only with alphanumeric symbols, ASCII 0-255
"""

from collections import Counter
from queue import PriorityQueue
import os

class HuffmanNode:
    def __init__(self, char, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def decode(encoded_text):
    """Returns decoded string"""

    encoded_text_ar = list(encoded_text)
    encoded_tree = _decode_huffman_tree(encoded_text_ar)

    # remove extra zeros
    number_of_extra_0_bin = encoded_text_ar[:8]                 # Agafa els primers 8 bits que indiquen la quantitat de zeros en binari
    encoded_text_ar = encoded_text_ar[8:]                       # Elimina els 8 primers bits d'informació
    number_of_extra_0 = int("".join(number_of_extra_0_bin), 2)  # Numero de zeros en decimal
    encoded_text_ar = encoded_text_ar[number_of_extra_0:]       # Elimina els extra zeros

    # decode text
    text = ""
    current_node = encoded_tree
    for char in encoded_text_ar:
        current_node = current_node.left if char == '0' else current_node.right

        if current_node.char is not None:
            text += current_node.char
            current_node = encoded_tree

    return text

def decompress(input_path, output_path):
    """Save decoded text to output file"""

    with open(input_path, "rb") as in_file, open(output_path, "w") as out_file:
        encoded_text = ""

        byte = in_file.read(1)
        while len(byte) > 0:
            encoded_text += f"{bin(ord(byte))[2:]:0>8}"
            byte = in_file.read(1)

        decoded_text = decode(encoded_text)
        out_file.write(decoded_text)

def _decode_huffman_tree(tree_code_ar):
    """Decoding huffman tree to be able to decode the encoded text"""

    # need to delete each use bit as we don't know the length of it and
    # can't separate it from the text code
    code_bit = tree_code_ar[0]
    del tree_code_ar[0]

    if code_bit == "1":
        char = ""
        for _ in range(8):
            char += tree_code_ar[0]
            del tree_code_ar[0]

        return HuffmanNode(chr(int(char, 2)))

    return HuffmanNode(None, left=_decode_huffman_tree(tree_code_ar), right=_decode_huffman_tree(tree_code_ar))


def _print_ratio(input_path, output_path):
    before_size = os.path.getsize(input_path)
    after_size = os.path.getsize(output_path)
    compression_percent = round(100 - after_size / before_size * 100, 1)

    print(f"\n-> Before: {before_size}bytes")
    print(f"-> After: {after_size}bytes")
    print(f"-> Compression {compression_percent}%")

if __name__ == "__main__":
    file_to_compress, decompressed, compressed = "compress-me-specific.txt", "decompressed_specific.txt", "compressed_specific.txt"
    _print_ratio(file_to_compress, compressed)
    decompress(compressed, decompressed)
    file_to_compress, decompressed, compressed = "compress-me-generic.txt", "decompressed_generic.txt", "compressed_generic.txt"
    _print_ratio(file_to_compress, compressed)
    decompress(compressed, decompressed)
