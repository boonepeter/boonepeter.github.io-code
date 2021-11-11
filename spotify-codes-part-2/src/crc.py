
def crc(data, polynomial):
    n = len(polynomial) - 1
    initial_length = len(data)
    check_bits = data + [0] * n
    for i in range(initial_length):
        if check_bits[i] == 1:
            for j, p in enumerate(polynomial):
                check_bits[i + j] = check_bits[i + j] ^ p
    return check_bits[-n:]

def check_crc(data, polynomial, check_bits):
    full_data = data + check_bits
    for i in range(len(data)):
        if full_data[i] == 1:
            for j, p in enumerate(polynomial):
                full_data[i + j] = full_data[i + j] ^ p
    return 1 not in full_data
data = [0,0,1,0,0,0,1,0,1,1,1,1,0,1,1,1,1,0,0,0,1,1,1,1,0,1,1,0,1,0,1,1,0,0,0,0,1,1,0,1]
check = [1,1,0,0,1,1,0,0]
poly = [1,0,0,0,0,0,1,1,1]
print(check_crc(data, poly, check))

if __name__ == "__main__":
    example = "0010001011110111100011110110101100001101"
    long = [int(i) for i in example]
    polynomial = [1, 0, 0, 0, 0, 0, 1, 1, 1] # crc8 polynomial
    check = crc(long, polynomial)
    print(f"Check bits: {check}")
    checked = check_crc(long, polynomial, check)
    print(f"Checked: {checked}")