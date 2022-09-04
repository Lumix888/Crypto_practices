#include <stdio.h>
#include <stdint.h>

#define BUFFSIZE 4096
#define ENCKEY 0x2D // here I set the key for 45 in exadecimal

void encrypt_file(FILE*, FILE*); //prototipe of the function to create the output file from the input
void encrypt(uint8_t*, size_t); //prototipe of the encrypt function using XOR


int main(int argc, const char* argv[])
{
    if (argc < 2) {//checking if the name of the file to encrypt is provvided in the commandline arguments 
        fprintf(stderr, "usage: %s <File>\n", argv[0]);
        return 1;
    }
    FILE* in_fp, * out_fp;

    if (fopen_s(&in_fp, argv[1], "rb") != 0) {//posssible error opening the input file
        fprintf(stderr, "Error in opening file %s\n", argv[1]);
        return 1;
    }
    if (fopen_s(&out_fp,  "out.txt", "wb") != 0) {//possible error in opening the output file
        fprintf(stderr, "Error in opening output\n");
        return 1;
    }

    encrypt_file(in_fp, out_fp);
    if (in_fp)
        fclose(in_fp);
    if (out_fp)
        fclose(out_fp);

    return 0;
}



void encrypt_file(FILE* in_fp, FILE* out_fp)
{
    uint8_t buf[BUFFSIZE];
    size_t n; // the number of items going to be read

    while ((n = fread(buf, sizeof(uint8_t), BUFFSIZE, in_fp)) != 0) {
        encrypt(buf, n);
        fwrite(buf, sizeof(uint8_t), n, out_fp);
    }
}


void encrypt(uint8_t* buf, size_t n)
{
    for (uint8_t* p = buf; p != buf + n; ++p)
        *p ^= ENCKEY; // ^= compute the XOR and assign it to the *p
}