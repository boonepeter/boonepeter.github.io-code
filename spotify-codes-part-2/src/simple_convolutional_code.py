from typing import List


def encode(bits: List[int], polynomial: List[int], tail_bite=False):
    """Convolutionally encode the stream of bits using the generator polynomial.
    If tail_bite == True, prepend the tail of the input. Otherwise use 0s to fill.
    """
    if tail_bite:
        tail = bits[-(len(polynomial) - 1):]
    else: 
        tail = [0 for i in range(len(polynomial) - 1)]
    full = tail + bits
    polynomial.reverse() # Reverse since we're working the other direction
    parity_bits = []
    for i in range(len(bits)):
        parity = 0
        for j in range(len(polynomial)):
            parity ^= full[i + j] * polynomial[j]
        parity_bits.append(parity)
    return parity_bits


if __name__ == "__main__":
    g0 = [1, 0, 1, 1, 0, 1, 1]
    g1 = [1, 1, 1, 1, 0, 0, 1]
    bits = "010001001110111111110001110101101011011001100"
    g0_expected = "100011100111110100110011110100000010001001011"
    g1_expected = "110011100010110110110100101101011100110011011"
    bits = [int(i) for i in bits]

    p0 = encode(bits, g0, True)
    p1 = encode(bits, g1, True)

    print(g0_expected == "".join(str(i) for i in p0))
    print(g1_expected == "".join(str(i) for i in p1))