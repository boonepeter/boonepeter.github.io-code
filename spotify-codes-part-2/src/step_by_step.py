



media_ref = 57639171874
binary = f"{bin(media_ref)[2:]:0>37}"
print(binary)
# pad with 3 bits to the right:
binary = f"{binary:0<39}"
print(binary)

a = "100011100111110100110011110100000010001001011"
b = "110011100010110110110100101101011100110011011"
c = zip(a, b)
print("".join(i + j for i, j in c))