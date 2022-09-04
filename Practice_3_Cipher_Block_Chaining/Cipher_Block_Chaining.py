#!/usr/bin/env python3

import os, sys
from Crypto.Cipher import AES
from Crypto.Util.strxor import strxor
from hashlib import pbkdf2_hmac
import hashlib, hmac


def padd_text(text):
    padd_len = 16 - len(text)%16 if len(text)%16 != 0 else 16 
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


def encrypt(pfile):
    password = input("Enter password: ").encode()
    salt = os.urandom(8)
    key = pbkdf2_hmac('sha1', password, salt, 1000, 16)

    with open(pfile, 'rb') as fp:
        plain_text = padd_text(fp.read())

    iv_vector = os.urandom(16)
    cipher = cbc_encrypt(plain_text, key, iv_vector)

    with open('encrypted.txt' , 'wb') as fp:
        fp.write(cipher)
    with open('iv_vector.txt' , 'wb') as fp:
        fp.write(iv_vector)
    with open('salt.txt' , 'wb') as fp:
        fp.write(salt)
    



def decrypt(cfile, vfile, sfile):
    with open(cfile, 'rb') as fp:
        cipher = fp.read()
    with open(vfile, 'rb') as fp:
        iv_vector = fp.read()
    with open(sfile, 'rb') as fp:
        salt = fp.read()
    
    password = input("Enter password: ").encode()

    key = pbkdf2_hmac('sha1', password, salt, 1000, 16)
    
    plain_text = cbc_decrypt(cipher, key, iv_vector)

    with open('plain.txt', 'wb') as fp:
        padd_len = plain_text[len(plain_text) - 1]
        fp.write(plain_text[: len(plain_text) - padd_len])


def usage():
    print("Usage:")
    print("-encrypt <plaintextfile>")
    print("-decrypt <ciphertextfile> <initializationvectorfile> <saltfile>")
    sys.exit(1)

print(sys.argv)
if len(sys.argv) == 3 and sys.argv[1] == '-encrypt':
    encrypt(sys.argv[2])
elif sys.argv[1] == '-decrypt' and len(sys.argv) == 5:
    decrypt(sys.argv[2], sys.argv[3], sys.argv[4])
else:
    usage()
