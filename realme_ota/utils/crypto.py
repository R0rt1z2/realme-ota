import base64
import hashlib
import json

from Crypto.Cipher import AES

# Keys
ENC_KEYS = ["09e32ji68RDaae6H", "404H8RDaae6HE8j"]
DEC_KEYS = ["oppo1997", "baed2017", "java7865", "231uiedn", "09e32ji6",
            "0oiu3jdy", "0pej387l", "2dkliuyt", "20odiuye", "87j3id7w"]

# Padding
BLOCK_SIZE = 16
PAD = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
UNPAD = lambda s: s[:-ord(s[len(s) - 1:])]

def encKey(buf, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return str(base64.encodebytes(cipher.encrypt(PAD(buf).encode())), encoding='utf-8')

def decKey(buf, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return UNPAD(cipher.decrypt(base64.b64decode(buf))).decode("utf-8")

def getKey(tail):
    return DEC_KEYS[int(tail[0])] + tail[4:12]
    
def encReq(data):
    return {'params':(encKey(str(data), ENC_KEYS[0]) + ENC_KEYS[1]).replace("\n", "")}

def decReq(data):
    return json.loads(decKey(data[:len(data) - 15], getKey(data[len(data) - 15:])))