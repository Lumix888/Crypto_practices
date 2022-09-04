#!/usr/bin/env python3

from random import randint

p = int(input("Enter p: "))
q = int(input("Enter q: "))
g = int(input("Enter g: "))

b = int(input("Enter Bob's public key: "))
m = int(input("Enter message: "))
while m <= 0 or m >= p - 1:
    print("Message m has to be 0 < m < p - 1")
    m = int(input("Enter message: ")) 


k = randint(2, p - 1)

c_1 = pow(g, k, p)
c_2 = (m * pow(b, k, p))%p


print("(%d, %d)"%(c_1, c_2))