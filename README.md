# Decrypto

A quick and dirty md5 bruteforcer to observe multiprocess computing

_Tested on Ubuntu 19.04 64 bits_

## Dependencies

### C

- GCC version 8.3.0 (Ubuntu 8.3.0-6ubuntu1)
- OpenSSL 1.1.1b  26 Feb 2019
- OpenMP 4.5

### Python

- Python 3.7.3

## Usage

### C

**For the single thread implementation (decrypto):**

Compile:
`$ gcc -o decrypto decrypto.c -lcrypto`

Usage:
`$ ./decrypto MD5 password_length`

**For the multiple thread implementation (mpdecrypto):**

_Note: this implementation use 4 threads_

Compile:
`$ gcc -o mpdecrypto mpdecrypto.c -lcrypto -fopenmp`

Usage:
`$ ./mpdecrypto MD5 password_length`

### Python

**For the single thread implementation (decrypto.py):**

Usage:
`$ ./decrypto.py MD5 password_length`

**For the multiprocess implementation (mpdecrypto.py):**

_Note: this implementation use 4 proccesses_

Usage:
`$ ./mpdecrypto MD5 password_length`
