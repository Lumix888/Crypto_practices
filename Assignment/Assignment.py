#!/usr/bin/env python3

import os, sys

sys.path = sys.path[1:]
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from hashlib import pbkdf2_hmac


def nb(i):
    b = []

    while True:
        b.append(i & ((1 << 8) - 1))
        i >>= 8
        if i == 0:
            break

    b.reverse()
    return bytes(b)

def get_keys(iter, password, salt=os.urandom(8)):
    key = pbkdf2_hmac('sha1', password, salt, iter, 16)
    return key[:16], salt

def padd_text(text):
    padd_len = 16 - len(text)%16
    return text + bytes([padd_len]*padd_len)

def cbc_encrypt(plain_text, key, iv_vector):
    cipher = AES.new(key)
    cipher_text = b''
    for i in range(0, len(plain_text), 16):
        cipher_block = cipher.encrypt(strxor(plain_text[i:i + 16], iv_vector))
        cipher_text += cipher_block
        iv_vector = cipher_block
    return cipher_text

def cbc_decrypt(cipher_text, key, iv_vector):
    cipher = AES.new(key)
    plain_text = b''
    for i in range(0, len(cipher_text), 16): 
        plain_text += strxor(cipher.decrypt(cipher_text[i:i + 16]), iv_vector)
        iv_vector = cipher_text[i:i + 16]
    return plain_text

def encrypt(pfile, cfile):
    iter = 1000

    password = input("Enter password: ").encode()
    key, salt = get_keys(iter, password) 

    with open(pfile, 'rb') as fp:
        plain_text = padd_text(fp.read())

    iv_vector = os.urandom(16)
    cipher = cbc_encrypt(plain_text, key, iv_vector)

    with open(cfile, 'wb') as fp:
        fp.write(salt + iv_vector + cipher)

def decrypt(cfile, pfile):
    iter = 1000

    with open(cfile, 'rb') as fp:
        c = fp.read()

    password = input("Enter password: ").encode()

    salt, iv_vector, cipher = c[:8], c[8:24], c[24:]

    key, _= get_keys(iter, password, salt)
    plain_text = cbc_decrypt(cipher, key, iv_vector)

    with open(pfile, 'wb') as fp:
        padd_len = plain_text[len(plain_text) - 1]
        fp.write(plain_text[: len(plain_text) - padd_len])

def usage():
    print("Usage:")
    print("-encrypt <plaintextfile> <ciphertextfile>")
    print("-decrypt <ciphertextfile> <plaintextfile>")
    sys.exit(1)


if len(sys.argv) != 4:
    usage()
elif sys.argv[1] == '-encrypt':
    encrypt(sys.argv[2], sys.argv[3])
elif sys.argv[1] == '-decrypt':
    decrypt(sys.argv[2], sys.argv[3])
else:
    usage()
