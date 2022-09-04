#include <stdio.h>
#include <stdlib.h>
#include <stdint.h> //this library is to get uint8_t, a type for a byte.

#define BUFFSIZE 4096 
#define MAXNAMELEN 40 //maximum lenght of the output file, 40 sounded fine

void decrypt_file(FILE*); // prototype of the function to 
void read_dec(FILE*, FILE*, uint8_t);
void decrypt(uint8_t*, size_t, uint8_t);



int main(int argc, const char* argv[])
{
    if (argc < 2) {
        fprintf(stderr, "usage: %s <File>\n", argv[0]);
        return 1;
    }
    FILE* fp;

    if (fopen_s(&fp, argv[1], "rb") != 0) {
        fprintf(stderr, "Error in opening file %s\n", argv[1]);
        return 1;
    }

    decrypt_file(fp);
    if (fp)
        fclose(fp);

    return 0;
}



void decrypt_file(FILE* fp)
{

    uint8_t key = 0x0;

    do {
        FILE* out_fp;
        char fname[MAXNAMELEN];

        sprintf_s(fname, MAXNAMELEN - 1, "key_%u.txt", key);
        if (fopen_s(&out_fp, fname, "wb") != 0) {
            fprintf(stderr, "Error in opening file %s\n", fname);
            exit(1);
        }
        read_dec(fp, out_fp, key);
        if (out_fp)
            fclose(out_fp);
        rewind(fp);
        ++key;
    } while (key != 0x0);

}


void read_dec(FILE* in_fp, FILE* out_fp, uint8_t key)
{

    uint8_t buf[BUFFSIZE];
    size_t n; // the number of items going to be read

    while ((n = fread(buf, sizeof(uint8_t), BUFFSIZE, in_fp)) != 0) {
        decrypt(buf, n, key);
        fwrite(buf, sizeof(uint8_t), n, out_fp);
    }
}

void decrypt(uint8_t* buf, size_t n, uint8_t key)
{
    for (uint8_t* p = buf; p != buf + n; ++p)
        *p ^= key; // ^= compute the XOR and assign it to the *p
}