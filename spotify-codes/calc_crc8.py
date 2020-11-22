import crc8

hash = crc8.crc8()
media_ref = 67775490487
ref_bytes = media_ref.to_bytes(5, byteorder="big")
print(ref_bytes)
# b'\x0f\xc7\xbb\xe9\xb7'
hash.update(ref_bytes)
check_bits = hash.digest()
print(check_bits)
# b'\x0c'