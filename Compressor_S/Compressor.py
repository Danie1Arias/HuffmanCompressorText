""" Implementation of archivator using Huffman coding works only with alphanumeric symbols, ASCII 0-255 """
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


def encode(text):
    """Returns encoded string code with format [encoded_huffman_tree][extra_zeros_num][encoded_text]"""

    frequencies = Counter(text)                                     # Calcular la freqüència de cada caràcter
    queue = PriorityQueue()                                         # Ordenar els caràcters en ordre de més a menys freqüència
    code_table = {}

    for char, f in frequencies.items():
        queue.put(HuffmanNode(char, f))                             # Crea un node on es relaciona la freqüència i el caràcter

    # merge nodes
    while queue.qsize() > 1:
        l, r = queue.get(), queue.get()
        queue.put(HuffmanNode(None, l.freq + r.freq, l, r))         # Agrupar els nodes fins que tots els símbols estàn relacionats

    huffman_tree = queue.get()
    huffman_tree 
    _fill_code_table(huffman_tree, "", code_table)                  # Afegeix la informació de la LUT al codi que s'envia per descomprimir

    encoded_text_code = ""
    array_text = list(text)
    i=0

    for c in text:                                                  # Relacionar el caràcter emb el codi de la LUT
        encoded_text_code += code_table[c]
        i= i + 1

    pass

    encoded_tree_code = _encode_huffman_tree(huffman_tree, "")      # Codifica la LUT 

    # add extra zeros, as in python it is not possible read
    # file bit by bit (min byte) so extra zeros will be
    # added automatically which cause a loss of information

    num = 8 - (len(encoded_text_code) + len(encoded_tree_code)) % 8 # Calcula els zeros que s'han d'afegir de més a més
    if num != 0:                                                    # Afegeix zeros al final per codificar en bytes
        encoded_text_code = num * "0" + encoded_text_code

    print("DATA:")
    print(f"-> Frequencies: {frequencies}")
    print(f"\n-> Charcter code: {code_table}")
    print(f"\n-> Encoded huffman tree code: {encoded_tree_code}")
    print(f"\n-> Encoded text code: {encoded_text_code}")

    return f"{encoded_tree_code}{num:08b}{encoded_text_code}"       # {num:08b} Especifica la quantitat de zeros afegits en binari

def compress(input_path, output_path):
    """Save encoded text to output file"""

    with open(input_path) as in_file, open(output_path, "wb") as out_file:
        text = in_file.read()                                           # Es llegeix el fitxer
        encoded_text = encode(text)                                     # Es comprimeix amb Huffman

        b_arr = bytearray()
        for i in range(0, len(encoded_text), 8):                        # Guardar les dades en bytes
            b_arr.append(int(encoded_text[i:i+8], 2))

        out_file.write(b_arr)

def _fill_code_table(node, code, code_table):
    """Fill code table, which has chars and corresponded codes"""

    if node.char is not None:
        code_table[node.char] = code
    else:
        _fill_code_table(node.left, code + "0", code_table)
        _fill_code_table(node.right, code + "1", code_table)


def _encode_huffman_tree(node, tree_text):
    """Encode huffman tree to save it in the file"""

    if node.char is not None:
        tree_text += "1"
        tree_text += f"{ord(node.char):08b}"
    else:
        tree_text += "0"
        tree_text = _encode_huffman_tree(node.left, tree_text)
        tree_text = _encode_huffman_tree(node.right, tree_text)

    return tree_text


if __name__ == "__main__":
    file_to_compress, compressed = "compress-me", "compressed"
    compress(file_to_compress, compressed)
