#!/usr/bin/env python3 


from math import sqrt
from itertools import count, islice
from functools import reduce
import sys


def is_prime(n):
    return n > 1 and all(n % i for i in islice(count(2), int(sqrt(n)-1)))

def read_prime(msg, diffs = []):
    n = int(input(msg))
    while not is_prime(n) or n in diffs:
        n = int(input(msg))
    return n


def read_pub_exp(msg, n, phi_n):
    e = int(input(msg))
    while e <= 1 or e >= phi_n or n % e == 0:
        e = int(input(msg))
    return e


def usage():
    print("Usage:")
    print("encrypt <plaintext file> <output ciphertext file>")
    print("decrypt <ciphertext file> <output plaintext file>")
    sys.exit(1)



def encrypt(plain_file, cipher_file, e, n):
    with open(plain_file, 'r') as fp:
        message = fp.read().upper()
    
    if len(message) == 0:
        return
    message = map(lambda x: ord(x) - ord('A'), message)
    message = reduce(lambda a, b: 10*a + b, message, 0)

    cipher = pow(message, e, n)
    
    with open(cipher_file, 'w') as fp:
        print(cipher, file=fp)


def decrypt(cipher_file, plain_filed, d, n):
    with open(cipher_file, 'r') as fp:
        cipher = int(fp.read())

    message = str(pow(cipher, d, n))
    message = bytes(map(lambda x: ord('A') + ord(x) - ord('0'), message))

    with open(plain_filed, 'wb') as fp:
        fp.write(message)


if len(sys.argv) != 4:
    usage()

p = read_prime("Insert a prime P: ")
q = read_prime("Insert a prime Q: ", [p])
n = p*q
phi_n = (p - 1)*(q - 1)
e = read_pub_exp("Insert the public exponent e: ", n, phi_n)

k = 2
d = int((k*phi_n + 1)/e)

if sys.argv[1] == 'encrypt':
    encrypt(sys.argv[2], sys.argv[3], e, n)
elif sys.argv[1] == 'decrypt':
    decrypt(sys.argv[2], sys.argv[3], d, n)
else:
    usage()
