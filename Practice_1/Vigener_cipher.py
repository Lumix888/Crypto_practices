import sys

def encryptVigener(inpString, key): 
    length = len(inpString)

    result = ""
    j = 0
    for i in range(length):
        if not inpString[i].isalpha():
            enc = inpString[i]
        else:
            enc = (ord(inpString[i]) - ord('A')) + (ord(key[j]) - ord('A'))
            enc = chr(enc%26 + ord('A'))
        result += enc
        j = (j + 1) % len(key)
    return result


def decryptVigener(inpString, key): 
    length = len(inpString)

    result = ""
    j = 0
    for i in range(length):
        if not inpString[i].isalpha():
            enc = inpString[i]
        else:
            enc = (ord(inpString[i]) - ord('A')) - (ord(key[j]) - ord('A'))
            enc = chr(enc%26 + ord('A'))
        result += enc
        j = (j + 1) % len(key)
    return result

if __name__ == '__main__': 
    mode = input("Do you want to encrypt or decrypt? [enc/dec]").strip()
    
    if mode != "enc" and mode != "dec":
        print("Invalid mode provided", file=sys.stderr)
        sys.exit(1)

    if mode == "enc":
        inputFile = input("Enter file to encrypt: ")
    else:
        inputFile = input("Enter file to decrypt: ")
    
    keyFile = input("Enter file with the key: ")
    outFile = input("Enter output file: ")

    with open(inputFile, "r") as fp:
        content = fp.read().upper() # Transform all input text in uppercase
    
    with open(keyFile, "r") as fp:
        # Transform all key in uppercase
        # Key does not have to contain any space
        key = fp.read().upper() 

    with open(outFile, "w") as fp:
        if mode == "enc":
            print(encryptVigener(content, key), file=fp)
        else:
            print(decryptVigener(content, key), file=fp)