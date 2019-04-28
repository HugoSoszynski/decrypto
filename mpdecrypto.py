#!/usr/bin/python3

import sys
import hashlib
from multiprocessing import Pool


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

def find_passwd(letter):
    passwd = letter + " " * (int(sys.argv[2]) - 1)
    final = letter + "~" * (int(sys.argv[2]) - 1)
    md5 = sys.argv[1]

    if test_md5(md5, passwd) is True:
        return passwd
    passwd = inc_char(passwd, 1)
    while passwd != final :
        if test_md5(md5, passwd) is True:
            return passwd
        passwd = inc_char(passwd, 1)
    
    return None

def psswd(letters):
    for i in letters:
        ret = find_passwd(i)
        if ret is not None:
            return ret
    
    return None

if __name__ == "__main__":
    # ./decrypto MD5 password_length
    if len(sys.argv) < 3:
        print("Usage: ./mpdecrypto MD5 password_length")
        exit(1)
    
    with Pool(processes=4) as pool:
        it = pool.imap(psswd, [[' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7'], ['8', '9', ':', ';', '<', '=', '>', '?', '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O'], ['P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g'], ['h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~']])
        for _ in range(95):
            tmp = next(it)
            if tmp is not None:
                print("Result: " + tmp)
                pool.terminate
                exit(0)

    print("Not Found")
