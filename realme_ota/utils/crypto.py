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

from Crypto.Cipher import AES
from Crypto.Util import Counter
from Crypto.Util.Padding import unpad, pad

keys = ["oppo1997", "baed2017", "java7865", "231uiedn", "09e32ji6",
        "0oiu3jdy", "0pej387l", "2dkliuyt", "20odiuye", "87j3id7w"]

def getKey(key):
    return (keys[int(key[0])] + key[4:12]).encode('utf-8')

def encrypt_ctr(buf):
    key_pseudo = str(randint(0, 9)) + ''.join(choices(string.digits, k=14))
    key_real = getKey(key_pseudo)

    ctr = Counter.new(128, initial_value=int.from_bytes(hashlib.md5(key_real).digest(), "big"))
    cipher = AES.new(key_real, AES.MODE_CTR, counter=ctr)
    encrypted = cipher.encrypt(buf.encode("utf-8"))

    return b64encode(encrypted).decode('utf-8') + key_pseudo

def decrypt_ctr(buf):
    data = b64decode(buf[:-15])
    key_real = getKey(buf[-15:])

    ctr = Counter.new(128, initial_value=int.from_bytes(hashlib.md5(key_real).digest(), "big"))
    cipher = AES.new(key_real, AES.MODE_CTR, counter=ctr)

    return cipher.decrypt(data).decode("utf-8")

def encrypt_ecb(buf):
    key_pseudo = str(randint(0, 9)) + ''.join(choices(string.ascii_letters + string.digits, k=14))
    key_real = getKey(key_pseudo)

    cipher = AES.new(key_real, AES.MODE_ECB)
    encrypted = cipher.encrypt(pad(buf.encode('utf-8'), AES.block_size))

    return b64encode(encrypted).decode('utf-8') + key_pseudo

def decrypt_ecb(buf):
    data = b64decode(buf[:-15])
    key = getKey(buf[-15:])

    cipher = AES.new(key, AES.MODE_ECB)
    plain = unpad(cipher.decrypt(data), AES.block_size)

    return plain.decode('utf-8')

def sha256(data):
    return hashlib.sha256(data.encode('utf-8')).hexdigest().upper()
