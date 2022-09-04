#!/usr/bin/env python3



p = int(input("Enter p: "))
q = int(input("Enter q: "))
g = int(input("Enter g: "))

b = int(input("Enter Bob's private key: "))


c_1 = int(input("Enter c1 from Alice: "))
c_2 = int(input("Enter c2 from Alice: "))




m = (pow(c_1, p - b - 1, p)*c_2)%p
print("Message: %d"%m)