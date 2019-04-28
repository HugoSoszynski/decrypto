#!/usr/bin/python3

import sys
import hashlib

def inc_char(passwd, index):
    if index >= int(sys.argv[2]):
        return passwd
    
    if passwd[index] == '~':
        ls = list(passwd)
        ls[index] = ' '
        passwd = "".join(ls)
        return inc_char(passwd, index + 1)

    ls = list(passwd)
    ls[index] = chr(ord(ls[index]) + 1)
    passwd = "".join(ls)
    return passwd

def test_md5(md5, passwd):
    if hashlib.md5(passwd.encode('utf-8')).hexdigest() == md5:
        return True
    return False

if __name__ == "__main__":
    # ./decrypto MD5 password_length
    if len(sys.argv) < 3:
        print("Usage: ./decrypto.py MD5 password_length")
        exit(1)
    
    passwd = " " * int(sys.argv[2])
    final = "~" * int(sys.argv[2])
    md5 = sys.argv[1]

    while passwd != final :
        if test_md5(md5, passwd) is True:
            print("Result: " + passwd)
            exit(0)
        passwd = inc_char(passwd, 0)
    if test_md5(md5, passwd) is True:
        print("Result: " + passwd)
        exit(0)
    
    print("Not found")
