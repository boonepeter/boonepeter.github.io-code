

from typing import List

def encode_simple(input_bits: List[int], g0=[1, 0], g1=[0,1]):
    memory = [0]
    output = []
    for i in input_bits:
        one = bool(g0[0] and i) ^ bool(g0[1] and memory[0])
        two = bool(g1[0] and i) ^ bool(g1[1] and memory[0])
        one = 1 if one else 0
        two = 1 if two else 0
        output.append([one, two])
        memory.pop()
        memory.append(i)
    return output


if __name__ == "__main__":
    input_bits = [1, 1, 0, 1, 1]
    output = encode_simple(input_bits)
    for o in output:
        print(o)