import sys
from time import sleep

def text_to_bin(text):
    return ''.join(f'{ord(char):08b}' for char in text)

def bin_to_text(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

def hex_to_bin(hex_str):
    bin_map = {
        '0': '0000', '1': '0001', '2': '0010', '3': '0011',
        '4': '0100', '5': '0101', '6': '0110', '7': '0111',
        '8': '1000', '9': '1001', 'A': '1010', 'B': '1011',
        'C': '1100', 'D': '1101', 'E': '1110', 'F': '1111'
    }
    return ''.join(bin_map[char] for char in hex_str)

def bin_to_hex(binary):
    hex_map = {
        '0000': '0', '0001': '1', '0010': '2', '0011': '3',
        '0100': '4', '0101': '5', '0110': '6', '0111': '7',
        '1000': '8', '1001': '9', '1010': 'A', '1011': 'B',
        '1100': 'C', '1101': 'D', '1110': 'E', '1111': 'F'
    }
    hex_str = ''
    for i in range(0, len(binary), 4):
        hex_str += hex_map[binary[i:i+4]]
    return hex_str

def bin_to_dec(binary):
    return sum(int(bit) * 2**(len(binary)-i-1) for i, bit in enumerate(binary))

def dec_to_bin(decimal):
    return bin(decimal)[2:].zfill(8)

def permute(key, arr, n):
    return ''.join(key[arr[i]-1] for i in range(n))

def shift_left(key, n):
    return key[n:] + key[:n]

def xor(a, b):
    return ''.join('0' if x == y else '1' for x, y in zip(a, b))
    ans = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            ans = ans + "0"
        else:
            ans = ans + "1"
    return ans

# permutation table
initial_perm = [58, 50, 42, 34, 26, 18, 10, 2,
                60, 52, 44, 36, 28, 20, 12, 4,
                62, 54, 46, 38, 30, 22, 14, 6,
                64, 56, 48, 40, 32, 24, 16, 8,
                57, 49, 41, 33, 25, 17, 9, 1,
                59, 51, 43, 35, 27, 19, 11, 3,
                61, 53, 45, 37, 29, 21, 13, 5,
                63, 55, 47, 39, 31, 23, 15, 7]


exp_d = [32, 1, 2, 3, 4, 5, 4, 5,
         6, 7, 8, 9, 8, 9, 10, 11,
         12, 13, 12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21, 20, 21,
         22, 23, 24, 25, 24, 25, 26, 27,
         28, 29, 28, 29, 30, 31, 32, 1]


per = [16,  7, 20, 21,
       29, 12, 28, 17,
       1, 15, 23, 26,
       5, 18, 31, 10,
       2,  8, 24, 14,
       32, 27,  3,  9,
       19, 13, 30,  6,
       22, 11,  4, 25]

# S-box Table
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
 
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
 
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
 
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
 
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
 
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
 
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
 
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]


# Final Permutation Table
final_perm = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

# Fungsi untuk mengenkripsi pesan
# Parameter:
# pt: Plaintext yang akan dienkripsi
# key_hex: Kunci dalam format heksadesimal
# Return: Ciphertext dalam format biner
def encrypt(pt, key_hex):
    pt = text_to_bin(pt)

    rkb = []
    rk = []
    rkb, rk = generate_round_keys(key_hex)

    #Initial Permutation
    pt = permute(pt, initial_perm, 64)
    print("\nAfter initial permutation", bin_to_hex(pt))

    #Splitting
    left = pt[0:32]
    right = pt[32:64]
    for i in range(0, 16):
        right_expanded = permute(right, exp_d, 48)
        xor_x = xor(right_expanded, rkb[i])
        sbox_str = ""
        for j in range(0, 8):
            row = bin_to_dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin_to_dec(int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
            val = sbox[j][row][col]
            sbox_str = sbox_str + dec_to_bin(val)
        sbox_str = permute(sbox_str, per, 32)

        #XOR kiri dan sbox_str
        result = xor(left, sbox_str)
        left = result 
        if(i != 15):
            left, right = right, left
        print("Round ", i+1, " ", bin_to_hex(left), " ", bin_to_hex(right), " ", rk[i])
        
    print("\n")
    #Combination
    combine = left + right
    chiper_text = permute(combine, final_perm, 64)
    return chiper_text

# Fungsi untuk mendekripsi pesan yang telah dienkripsi
# Parameter:
# ct: Ciphertext dalam format heksadesimal
# key_hex: Kunci dalam format heksadesimal
# Return: Plaintext dalam format biner
def decrypt(ct, key_hex):
    ct = hex_to_bin(ct)
    rkb = []
    rk = []
    rkb, rk = generate_round_keys(key_hex)

    # Initial Permutation
    ct = permute(ct, initial_perm, 64)
    print("After initial permutation:", bin_to_hex(ct))

    # Splitting
    left = ct[0:32]
    right = ct[32:64]
    for i in range(15, -1, -1):  
        right_expanded = permute(right, exp_d, 48)
        xor_x = xor(right_expanded, rkb[i])
        sbox_str = ""
        for j in range(0, 8):
            row = bin_to_dec(int(xor_x[j * 6] + xor_x[j * 6 + 5]))
            col = bin_to_dec(int(xor_x[j * 6 + 1] + xor_x[j * 6 + 2] + xor_x[j * 6 + 3] + xor_x[j * 6 + 4]))
            val = sbox[j][row][col]
            sbox_str = sbox_str + dec_to_bin(val)
        sbox_str = permute(sbox_str, per, 32)

        # XOR left and sbox_str
        result = xor(left, sbox_str)
        left = result

        # Swapper
        if i != 0: 
            left, right = right, left

        print("Round", 16 - i, bin_to_hex(left), bin_to_hex(right), rk[i])

    # final combination
    combine = left + right

    # final permutate
    plain_text = permute(combine, final_perm, 64)
    return plain_text

#generate key
def generate_round_keys(key_hex):
    #hex to bin
    key_binary = hex_to_bin(key_hex)

    #table for key
    keyp = [57, 49, 41, 33, 25, 17, 9,
            1, 58, 50, 42, 34, 26, 18,
            10, 2, 59, 51, 43, 35, 27,
            19, 11, 3, 60, 52, 44, 36,
            63, 55, 47, 39, 31, 23, 15,
            7, 62, 54, 46, 38, 30, 22,
            14, 6, 61, 53, 45, 37, 29,
            21, 13, 5, 28, 20, 12, 4]
    key_binary = permute(key_binary, keyp, 56)

    # Number of bit shifts
    shift_table = [1, 1, 2, 2,
                   2, 2, 2, 2,
                   1, 2, 2, 2,
                   2, 2, 2, 1]

    key_comp = [14, 17, 11, 24, 1, 5,
                3, 28, 15, 6, 21, 10,
                23, 19, 12, 4, 26, 8,
                16, 7, 27, 20, 13, 2,
                41, 52, 31, 37, 47, 55,
                30, 40, 51, 45, 33, 48,
                44, 49, 39, 56, 34, 53,
                46, 42, 50, 36, 29, 32]

    # Splitting
    left = key_binary[0:28]
    right = key_binary[28:56]

    rkb = []  #RoundKeys on biner
    rk = []  #RoundKeys on hexadecimal
    for i in range(0, 16):
        
        left = shift_left(left, shift_table[i])
        right = shift_left(right, shift_table[i])

        #combine left and right
        combine_str = left + right

        round_key = permute(combine_str, key_comp, 48)

        rkb.append(round_key)
        rk.append(bin_to_hex(round_key))

    return rkb, rk

#funcition for sending message
def sending():
    print("\nSending ", end="")
    for _ in range(5):
        sleep(0.4)
        print(".", end="")
        sys.stdout.flush()
    print(' SENT')