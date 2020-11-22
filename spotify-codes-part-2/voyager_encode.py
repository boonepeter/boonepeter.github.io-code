
from typing import List

G0 = [1, 1, 1, 1, 0, 0, 1]
G1 = [1, 0, 1, 1, 0, 1, 1]


def encode_bit(memory: List[int], poly: List[int]):
    total = False
    for i in range(len(memory)):
        total = total ^ bool(memory[i] and poly[i])
    return 1 if total else 0

def encode(input_bits: List[int], polynomials: List[List[int]]=[G0, G1]):
    # initialize
    memory = [0 for i in range(len(polynomials[0]))]
    output = []
    for i in input_bits:
        memory.pop()
        memory.insert(0, i)
        row = []
        for p in polynomials:
            row.append(encode_bit(memory, p))
        output.append(row)
    return output

if __name__ == "__main__":
    output = encode([1, 1, 0, 1, 1], [[1], [1]])
    for o in output:
        print(o)
