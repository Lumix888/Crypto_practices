def encryptDecryptXOR(inpString, xorKey): 
  
    length = len(inpString) 

    result = []
    j = 0
    for i in range(length):
        enc = inpString[i] ^ xorKey[j]
        result.append(enc)
        j = (j + 1) % len(xorKey)
    return bytes(result)

if __name__ == '__main__': 
    inputFile = input("Enter file to encrypt/decrypt: ")
    keyFile = input("Enter file with the key: ")
    outFile = input("Enter output file: ")

    with open(inputFile, "rb") as fp:
        content = fp.read()
    
    with open(keyFile, "rb") as fp:
        key = fp.read()

    with open(outFile, "wb") as fp:
        fp.write(encryptDecryptXOR(content, key))
