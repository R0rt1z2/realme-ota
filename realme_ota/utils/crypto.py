#
# This file is part of realme-ota (https://github.com/R0rt1z2/realme-ota).
# Copyright (c) 2022 Roger Ortiz.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#

import string
import hashlib

from base64 import b64decode, b64encode
from random import randint, choices

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util import Counter
from Crypto.Util.Padding import unpad, pad
from Crypto.Random import get_random_bytes

keys = ["oppo1997", "baed2017", "java7865", "231uiedn", "09e32ji6",
        "0oiu3jdy", "0pej387l", "2dkliuyt", "20odiuye", "87j3id7w"]

def getKey(key):
    return (keys[int(key[0])] + key[4:12]).encode('utf-8')

def getRandomKey():
    return get_random_bytes(32) # AES-256 key

def getIV():
    return get_random_bytes(16) # AES IV

def enc_dec_AES_CTR(data, key, iv, mode):
    ctr = Counter.new(128, initial_value=int.from_bytes(iv, 'big'))
    cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
    if mode == 'encrypt':
        return cipher.encrypt(data)
    else:
        return cipher.decrypt(data)

def enc_AES_CTR(data, key, iv):
    return enc_dec_AES_CTR(data, key, iv, 'encrypt')

def dec_AES_CTR(data, key, iv):
    return enc_dec_AES_CTR(data, key, iv, 'decrypt')

def enc_dec_AES_ECB(data, key, mode):
    cipher = AES.new(key, AES.MODE_ECB)
    if mode == 'encrypt':
        return cipher.encrypt(pad(data, AES.block_size))
    else:
        return unpad(cipher.decrypt(data), AES.block_size)

def enc_AES_ECB(data, key):
    return enc_dec_AES_ECB(data, key, 'encrypt')

def dec_AES_ECB(data, key):
    return enc_dec_AES_ECB(data, key, 'decrypt')

def encrypt_ctr_v2(data):
    key = getRandomKey()
    iv = getIV()
    encrypted = enc_AES_CTR(data.encode('utf-8'), key, iv)
    return b64encode(encrypted).decode('utf-8'), b64encode(iv).decode('utf-8'), b64encode(key).decode('utf-8')

def decrypt_ctr_v2(data, key, iv):
    return dec_AES_CTR(b64decode(data.encode('utf-8')), b64decode(key.encode('utf-8')), b64decode(iv.encode('utf-8')))

def encrypt_ctr(buf):
    key_pseudo = str(randint(0, 9)) + ''.join(choices(string.digits, k=14))
    key_real = getKey(key_pseudo)
    
    encrypted = enc_AES_CTR(buf.encode('utf-8'), key_real, hashlib.md5(key_real).digest())

    return b64encode(encrypted).decode('utf-8') + key_pseudo

def decrypt_ctr(buf):
    data = b64decode(buf[:-15])
    key_real = getKey(buf[-15:])

    decrypted = dec_AES_CTR(data, key_real, hashlib.md5(key_real).digest())

    return decrypted.decode('utf-8')

def encrypt_ecb(buf):
    key_pseudo = str(randint(0, 9)) + ''.join(choices(string.ascii_letters + string.digits, k=14))
    key_real = getKey(key_pseudo)
    
    encrypted = enc_AES_ECB(buf.encode('utf-8'), key_real)
    
    return b64encode(encrypted).decode('utf-8') + key_pseudo

def decrypt_ecb(buf):
    data = b64decode(buf[:-15])
    key = getKey(buf[-15:])
    
    plain = dec_AES_ECB(data, key)

    return plain.decode('utf-8')

def sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest().upper()

def encrypt_rsa(data, pub_key):
    key = RSA.import_key(pub_key)
    cipher = PKCS1_OAEP.new(key)
    return cipher.encrypt(data)

def generate_protectedKey(key, pub_key):
    encrypted = encrypt_rsa(key.encode('utf-8'), b64decode(pub_key.encode('utf-8')))
    return b64encode(encrypted).decode('utf-8')
