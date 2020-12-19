import numpy as np
import crccheck

# This code was written by "Doyle" on Stack Overflow
# https://stackoverflow.com/a/64950150/10703868


# Utils for conversion between int, array of binary
# and array of bytes (as ints)
def int_to_bin(num, length, endian):
    if endian == 'l':
        return [num >> i & 1 for i in range(0, length)]
    elif endian == 'b':
        return [num >> i & 1 for i in range(length-1, -1, -1)]

def bin_to_int(bin,length):
    return int("".join([str(bin[i]) for i in range(length-1,-1,-1)]),2)

def bin_to_bytes(bin, length):
    b = bin[0:length] + [0] * (-length % 8)
    return [(b[i]<<7) + (b[i+1]<<6) + (b[i+2]<<5) + (b[i+3]<<4) + 
        (b[i+4]<<3) + (b[i+5]<<2) + (b[i+6]<<1) + b[i+7] for i in range(0,len(b),8)]
    
# Return the circular right shift of an array by 'n' positions    
def shift_right(arr, n):
    return arr[-n % len(arr):len(arr):] + arr[0:-n % len(arr)]

gray_code = [0,1,3,2,7,6,4,5]
gray_code_inv = [[0,0,0],[0,0,1],[0,1,1],[0,1,0],
                 [1,1,0],[1,1,1],[1,0,1],[1,0,0]]

# CRC using Rocksoft model: 
# NOTE: this is not quite any of their predefined CRC's
# 8: number of check bits (degree of poly)
# 0x7: representation of poly without high term (x^8+x^2+x+1)
# 0x0: initial fill of register
# True: byte reverse data
# True: byte reverse check
# 0xff: Mask check (i.e. invert)
spotify_crc = crccheck.crc.Crc(8, 0x7, 0x0, True, True, 0xff)

def calc_spotify_crc(bin37):
    bytes = bin_to_bytes(bin37, 37)
    return int_to_bin(spotify_crc.calc(bytes), 8, 'b')

def check_spotify_crc(bin45):
    data = bin_to_bytes(bin45,37)
    return spotify_crc.calc(data) == bin_to_bytes(bin45[37:], 8)[0]

# Simple convolutional encoder
def encode_cc(dat):
    gen1 = [1,0,1,1,0,1,1]
    gen2 = [1,1,1,1,0,0,1]
    punct = [1,1,0]
    dat_pad = dat[-6:] + dat # 6 bits are needed to initialize
                             # register for tail-biting
    stream1 = np.convolve(dat_pad, gen1, mode='valid') % 2
    stream2 = np.convolve(dat_pad, gen2, mode='valid') % 2
    enc = [val for pair in zip(stream1, stream2) for val in pair]
    return [enc[i] for i in range(len(enc)) if punct[i % 3]]
    
# To create a generator matrix for a code, we encode each row
# of the identity matrix. Note that the CRC is not quite linear
# because of the check mask so we apply the lamda function to
# invert it. Given a 37 bit media reference we can encode by
#     ref * spotify_generator + spotify_mask (mod 2)
_i37 = np.identity(37, dtype=bool)
crc_generator = [_i37[r].tolist() + 
          list(map(lambda x : 1-x, calc_spotify_crc(_i37[r].tolist())))
          for r in range(37)]
spotify_generator = 1*np.array([encode_cc(crc_generator[r]) for r in range(37)], dtype=bool)  
del _i37

spotify_mask = 1*np.array(encode_cc(37*[0] + 8*[1]), dtype=bool) 
    
# The following matrix is used to "invert" the convolutional code.
# In particular, we choose a 45 vector basis for the columns of the
# generator matrix (by deleting those in positions equal to 2 mod 4)
# and then inverting the matrix. By selecting the corresponding 45 
# elements of the convolutionally encoded vector and multiplying 
# on the right by this matrix, we get back to the unencoded data,
# assuming there are no errors.
# Note: numpy does not invert binary matrices, i.e. GF(2), so we
# hard code the following 3 row vectors to generate the matrix.
conv_gen = [[0,1,0,1,1,1,1,0,1,1,0,0,0,1]+31*[0],
            [1,0,1,0,1,0,1,0,0,0,1,1,1] + 32*[0],
            [0,0,1,0,1,1,1,1,1,1,0,0,1] + 32*[0] ]

conv_generator_inv = 1*np.array([shift_right(conv_gen[(s-27) % 3],s) for s in range(27,72)], dtype=bool) 


# Given an integer media reference, returns list of 20 barcode levels
def spotify_bar_code(ref):
    bin37 = np.array([int_to_bin(ref, 37, 'l')], dtype=bool)
    enc = (np.add(1*np.dot(bin37, spotify_generator), spotify_mask) % 2).flatten()
    perm = [enc[7*i % 60] for i in range(60)]
    return [gray_code[4*perm[i]+2*perm[i+1]+perm[i+2]] for i in range(0,len(perm),3)]
    
# Equivalent function but using CRC and CC encoders.
def spotify_bar_code2(ref):
    bin37 = int_to_bin(ref, 37, 'l')
    enc_crc = bin37 + calc_spotify_crc(bin37)
    enc_cc = encode_cc(enc_crc)
    perm = [enc_cc[7*i % 60] for i in range(60)]
    return [gray_code[4*perm[i]+2*perm[i+1]+perm[i+2]] for i in range(0,len(perm),3)]
    
# Given 20 (clean) barcode levels, returns media reference
def spotify_bar_decode(levels):
    level_bits = np.array([gray_code_inv[levels[i]] for i in range(20)], dtype=bool).flatten()
    conv_bits = [level_bits[43*i % 60] for i in range(60)]
    cols = [i for i in range(60) if i % 4 != 2] # columns to invert
    conv_bits45 = np.array([conv_bits[c] for c in cols], dtype=bool)
    bin45 = (1*np.dot(conv_bits45, conv_generator_inv) % 2).tolist()
    if check_spotify_crc(bin45):
        return bin_to_int(bin45, 37)
    else:
        print('Error in levels; Use real decoder!!!')
        return -1