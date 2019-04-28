#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <openssl/md5.h>
#include <omp.h>

/*
** Dependencies:
**   - OpenSSL library
**   - OpenSSL develoment files (.h)
**
** To compile use the following line:
** $ gcc -o mpdecrypto mpdecrypto.c -lcrypto -fopenmp
*/

// Init the passord string for bruteforce
void init_passwd(char* passwd, size_t length) {
    for (size_t i = 0; i < length; ++i) {
        passwd[i] = ' ';
    }
}

// Increment the char in the string in a recursive way
char* inc_char(char* passwd, size_t length, size_t index) {
    if (index >= length)
        return passwd;
    if (passwd[index] == '~') {
        passwd[index] = ' ';
        return inc_char(passwd, length, index + 1);
    }
    passwd[index] += 1;
    return passwd;
}

// Return 1 on match, 0 otherwise
int test_md5(char* md5, char* passwd) {
    unsigned char digest[16];
    char hex[32];
    MD5_CTX ctx;

    MD5_Init(&ctx);
    MD5_Update(&ctx, passwd, strlen(passwd));
    MD5_Final(digest, &ctx);
    for (int i = 0; i < 16; ++i) {
        sprintf(&hex[i*2], "%02x", (unsigned int)digest[i]);
    }
    if (memcmp(hex, md5, 32) == 0)
        return 1;
    return 0;
}

// Return 1 if the string is full of the last tested char '~'
// 0 otherwise
int is_final(const char* passwd, size_t index) {
    int i = index;

    while (passwd[i] != '\0') {
        if (passwd[i] != '~')
            return 0;
        ++i;
    }
    return 1;
}

void write_result(char* passwd) {
    write(1, "Result: ", 8);
    write(1, passwd, strlen(passwd));
    write(1, "\n", 1);
}

void init_letters(char* letters) {
    for (int i = 0; i < 95; ++i) {
        letters[i] = 32 + i;
    }
}

int main(int ac, char** av) {
    char letters[95];
    size_t length;
    char* md5;
    char* passwd;
    int i;

    if (ac < 3) {
        write(2, "Usage: ./decrypto md5 password_length\n", 38);
        return 1;
    }
    init_letters(letters);
    md5 = av[1];
    length = atol(av[2]);
    #pragma omp parallel private(i, passwd) num_threads(4)
    {
        if ((passwd = calloc(length+1, 1)) == NULL) {
            write(2, "Unable to allocate memory\n", 26);
            exit(2);
        }
        int chunk_size = 95 / 4;
        int tid = omp_get_thread_num();
        int start = tid * chunk_size;
        int end = tid == 3 ? 94 : (tid + 1) * chunk_size - 1;
        for (i = start; i <= end; ++i) {
            init_passwd(passwd, length);
            passwd[0] = letters[i];
            while (!is_final(passwd, 1)) {
                if (test_md5(md5, passwd)) {
                    write_result(passwd);
                    exit(0); // I know passwd is not freed but we end the program
                }
                inc_char(passwd, length, 1);
            }
            // Check the last combinaison
            if (test_md5(md5, passwd)) {
                write_result(passwd);
                exit(0); // I know passwd is not freed but we end the program
            }
        }
        free(passwd);
    }
    return 0;
}