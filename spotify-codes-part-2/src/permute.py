


def permute(bits, step=7):
    for i in range(len(bits)):
        yield bits[(i * step) % len(bits)]

if __name__ == "__main__":
    bits = "111000111100101111101110111001011100110000100100011100110011"
    print("".join(permute(bits)))
    # 111100110001110101101000011110010110101100111111101000111000
