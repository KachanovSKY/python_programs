import math
import numpy as np

def is_prime(n):
    if n == 2 or n == 3:
        return True
    if n == 1 or n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

def primitive_root(p):
    if not is_prime(p):
        return None
    factors = [i for i in range(1, p) if p % i == 0]
    for g in range(1, p):
        if all(pow(g, (p - 1) // f, p) != 1 for f in factors):
            return g
    return None


def hash(astring, p):
        sum = 0
        for pos in range(len(astring)):
            sum = sum + ord(astring[pos])    
        return sum % p

def main():
    p = int(input("Enter open key (mod): "))# 1367#11969/15199	

    a = int(input("Enter secret key (a): "))#5479#11299 #secret key

    #af =int(input("Enter open key (af): "))# 977#8192

    af = primitive_root(p)

    y = pow(af, a, p)

    print ("Open keys: (", y, af, p, ")")

    m = input("Enter messege: ")
    H = hash(m, p)
    k = int(input("Enter open key (k): ")) #1103#10139
    ''' #''' 
    r = pow(af, k, p)

    k_1 = 2635#4607#2635
    s = (k_1 * ((H - a * r) % (p - 1))) % (p - 1)
    print("Signe keys: (", r, s, ")")

    if (pow(y, r, p) * pow(r, s, p)) % p == pow(af, H, p):
        print ("Signe is True")
    else:
        print ("Signe is True")

if __name__ == "__main__":
    main()
