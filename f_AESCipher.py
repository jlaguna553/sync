# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
import binascii
import Padding
llave = '05160f048ec6f52e924837c2bf84d665'
vector = 'd24ac216d2292c8f'

def encrypt(plaintext = '',key = llave,iv = vector):
    if plaintext != '':
        plaintext = Padding.appendPadding(plaintext,blocksize=Padding.AES_blocksize,mode=0)
        encobj = AES.new(key,AES.MODE_OFB,iv)
        return(binascii.b2a_base64(encobj.encrypt(plaintext)))
    else:
        return plaintext

def decrypt(ciphertext = '',key = llave,iv = vector):
    if ciphertext != '':
        cipher = binascii.a2b_base64(ciphertext)
        encobj = AES.new(key,AES.MODE_OFB,iv)
        return(Padding.removePadding(encobj.decrypt(cipher),mode=0))
    else:
        return ciphertext

