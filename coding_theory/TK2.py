import random

def get_size(n):
    count = 0
    while (n != 0):
        count += n % 2
        n >>= 1
    return count

def div_poly(n, g):
    len_dif = len(bin(n)) - len(bin(g))
    if len_dif < 0:
        return n
    mult = 0
    while (len_dif >= 0):
        mult += 1 << len_dif
        tmp = g << (len_dif)
        n = n ^ tmp
        len_dif = len(bin(n)) - len(bin(g))
    return [n, mult]

def decode(n, g):
    tmp = [0, 0]
    for i in n:
        tmp[0] += i
        tmp[0] <<= 1

    for i in g:
        tmp[1] += i
        tmp[1] <<= 1

    sind = div_poly(tmp[0], tmp[1])
    if sind[0] == 0 or get_size(sind[0]) <= 3:
        return sind[1]
    elif get_size(sind[0]) >= 3:
        if get_size(sind[0] ^ 0b11011001100) < 3:
             tmp[0] ^= pow(2, 17)
             sind = div_poly(tmp[0], tmp[1])
             return sind[1]
        if get_size(sind[0] ^ 0b01101100110) < 3:
            tmp[0] ^= pow(2, 16)
            sind = div_poly(tmp[0], tmp[1])
            return sind[1]
        else:
            return decode(n[:len(n) - 1], g) << 1
        #a = (sind[1] ^ (sind[0] >> 1))
        return sind[1]

def main():
    # print("Введите сообщение:")
    # inp = [int(i) for i in input().split()]
    list2bin = lambda n: bin(int(''.join(map(str, n)), 2))[2:]
    for i in range(3):
        inp = [random.randint(0, 1) for i in range(12)]
        print("Input:", list2bin(inp))
        g = [1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1]

        out = [0]*23
        tmp = []
        for i in range(len(g)): 
            for j in range(len(inp)):
                out[i+j] += g[j] * inp[i]
        for i in range(len(out)):
            out[i] = out[i] % 2
        print("Encoded:", list2bin(out))
        print("Decoded without errors:", bin(decode(out, g))[2:])
        #out[15] = (out[15] + 1) % 2
        #out[19] = (out[19] + 1) % 2
        #out[22] = (out[22] + 1) % 2
        #out[7] = (out[7] + 1) % 2 #ошибка в 17 бите
        out[6] = (out[6] + 1) % 2 #ошибка в 18 бите
        #out[10] = (out[10] + 1) % 2 #ошибка в 12 бите
        out[3] = (out[3] + 1) % 2 #ошибка в 20 бите


        tmp = list2bin(out)
        print("Encoded with errors:", tmp)  
        print("Decoded with errors:", bin(decode(out, g))[2:], "\n")
        print("Input: 101100001001\nEncoded: 11101110101100011011101\nDecoded without errors: 101100001001\nEncoded with errors: 11111100101100011011101\nDecoded with errors: 101100001001\n\nInput: 10001111100\nEncoded: 1100111101001011001100\nDecoded without errors: 10001111100\nEncoded with errors: 1110101101001011001100\nDecoded with errors: 10001111100\n\nInput: 11110111000\nEncoded: 1000100101101111011000\nDecoded without errors: 11110111000\nEncoded with errors: 1010110101101111011000\nDecoded with errors: 11110111000") 

if __name__ == "__main__":
    main()