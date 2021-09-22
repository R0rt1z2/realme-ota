import requests
import urllib.parse
import datetime
import time
import sys
import base64
import hashlib
import json

from Crypto.Cipher import AES

# Dummy IMEI
IMEI = "000000000000000"

# Keys
ENC_KEYS = ["09e32ji68RDaae6H", "404H8RDaae6HE8j"]
DEC_KEYS = ["oppo1997", "baed2017", "java7865", "231uiedn", "09e32ji6",
            "0oiu3jdy", "0pej387l", "2dkliuyt", "20odiuye", "87j3id7w"]

# Crypto padding
BLOCK_SIZE = 16
PAD = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
UNPAD = lambda s: s[:-ord(s[len(s) - 1:])]

# Default program usage
USAGE = f'''{sys.argv[0]} ro.product.name ro.build.version.ota'''

# Logging verbosity
LOGGING_LEVELS = {
    "-1":"U", # Unknown (Default)
    "0":"I",  # Info
    "1":"W",  # Warning
    "2":"E",  # Error
    "3":"F",  # Fatal Error
    "4":"D",  # Debug
    "5":"V",  # Verbose
}

def log(buf, prio = 0):
    line = f"[{datetime.datetime.now()}] "
    
    if (prio := str(prio)) in LOGGING_LEVELS:
        line += f"{LOGGING_LEVELS[prio]}: "
    else:
        line += "U: "

    line += f"{buf}"
    print(line)

def encKey(buf, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return str(base64.encodebytes(cipher.encrypt(PAD(buf).encode())), encoding='utf-8')

def decKey(buf, key):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    return UNPAD(cipher.decrypt(base64.b64decode(buf))).decode("utf-8")

def getKey(tail):
    return DEC_KEYS[int(tail[0])] + tail[4:12]

def main():
    PRODUCT = sys.argv[1]
    OTA_VERSION = sys.argv[2]

    if ("RMX" not in PRODUCT or "RMX" not in OTA_VERSION):
        log(f"Invalid values: {PRODUCT} - {OTA_VERSION}!", 2)
        exit(1)

    PRODUCT_IDENTIFIER = OTA_VERSION.split(".")[1]
    if not PRODUCT_IDENTIFIER.isalpha():
        log(f"Invalid product identifier: {PRODUCT_IDENTIFIER}!", 2)

    log(f"Device: {PRODUCT}")
    log(f"Major version: {OTA_VERSION[:15]}")
    log(f"Minor version: {OTA_VERSION[16:]}")
    log(f"Product identifier: {PRODUCT_IDENTIFIER}")

    TIME = str(time.time()).split(".")[0]
    DATA = '{"version": "2", "otaVersion": "OTA_VERSION", "imei": "IMEI", "mode": "0", "language": "en-US", "productName": "PRODUCT", "type": "1", "romVersion": "MINOR_VERSION", "colorOSVersion": "null", "androidVersion": "null", "time": TIME, "registrationId": "UNKNOWN", "operator": "NULL", "trackRegion": "null", "uRegion": "null", "ota_system_root_state": "1", "ota_register_trigger_id": "UNKNOWN", "isRooted": "1", "canCheckSelf": "1", "otaPrefix": "MINOR_VERSION" }'.replace("OTA_VERSION", 
            OTA_VERSION).replace("IMEI", IMEI).replace("PRODUCT", PRODUCT).replace("MINOR_VERSION", OTA_VERSION[:15]).replace("TIME", str(TIME))
    
    # Encrypt the request
    ENCRYPTED_DATA = encKey(str(DATA), ENC_KEYS[0]) + ENC_KEYS[1]
    ENCRYPTED_DATA = ENCRYPTED_DATA.replace("\n", "")
    
    # Generate the encrypted request
    ENCRYPTED_REQUEST = {'params':f'{ENCRYPTED_DATA}'}
    
    # Ask for the file
    headers = {'Accept': 'application/json', 'User-Agent': 'NULL', 'Content-Type' : 'application/json'}
    response = requests.post("https://ifota.realmemobile.com/post/Query_Update", data=json.dumps(ENCRYPTED_REQUEST), headers=headers)
    
    # Sanity Check
    assert response.status_code == 200
    
    # We just care about the encrypted response
    RAW_RESP = response.content.decode("utf-8").split(':"')[1]
    RAW_RESP = RAW_RESP[:len(RAW_RESP) - 2]

    # Get the tail
    RESPONSE_DATA = RAW_RESP[:len(RAW_RESP) - 15]
    RESPONSE_TAIL = RAW_RESP[len(RAW_RESP) - 15:]

    # Calculate the decrypt key
    DEC_KEY = getKey(RESPONSE_TAIL)
    log(f"Using {DEC_KEY} to decrypt the response...")
    
    # Decrypt the response
    DECRYPTED_RESPONSE = json.dumps(decKey(RESPONSE_DATA, DEC_KEY), indent=4, sort_keys=True)
    log(DECRYPTED_RESPONSE)
    
    exit(0)

if __name__ == '__main__':
    exit(USAGE) if (len(sys.argv) < 3) or (sys.argv[1] == "-h") else main()