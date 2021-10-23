#!/usr/bin/python3

import requests
import time
import sys
import json

from argparse import ArgumentParser

try:
    from utils import logger
    from utils import config
    from utils import crypto

except ImportError:
    from realme_ota.utils import logger
    from realme_ota.utils import config
    from realme_ota.utils import crypto

def die(msg, ec, log_level = 0):
    logger.log(f"{msg}", log_level)
    exit(ec)

def main():
    parser = ArgumentParser()
    parser.add_argument("product_model", type=str, help="Product Model (ro.product.name).")
    parser.add_argument("ota_version", help="OTA Version (ro.build.version.ota).")
    parser.add_argument("rui_version", type=int, choices=[1, 2], help="RealmeUI Version (ro.build.version.realmeui).")
    parser.add_argument("-c", "--server", type=int, default=0, help="Use specific server for the request (GL = 0, CN = 1, IN = 2, EU = 3).")
    parser.add_argument("-t", "--timeout", type=int, help="Use custom timeout for the request.")
    parser.add_argument("-d", "--dump", type=str, help="Save request response into file.")
    parser.add_argument("-o", "--only", type=str, help="Only show the desired value from the request.")
    parser.add_argument("-s", "--silent", action="store_true", help="Enable silent output (purge logging).")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1], default=1, help="Increase or decrease verbosity.")

    args = parser.parse_args()

    if args.verbosity == 0:
        logger.init(0)        
    else:
        logger.init(1)
        
    PRODUCT = args.product_model
    OTA_VERSION = args.ota_version
    PRODUCT_IDENTIFIER = OTA_VERSION.split(".")[1]
    TIME = str(time.time()).split(".")[0]
    MINOR_VERSION = OTA_VERSION[:15]
    MAJOR_VERSION = OTA_VERSION[13:]
    TIMEOUT = config.TIMEOUT
        
    if PRODUCT != OTA_VERSION[:7]:
        PRODUCT = OTA_VERSION[:7]
    
    if args.rui_version == 1:
        URL = config.RUI1_ENDPS["GL_URL"]
    elif args.rui_version == 2:
        URL = config.RUI2_ENDPS["GL_URL"]

    if args.server == 1:
        if args.rui_version == 1:
            URL = config.RUI1_ENDPS["CN_URL"]
        elif args.rui_version == 1:
            URL = config.RUI2_ENDPS["CN_URL"]
    elif args.server == 2:
        if args.rui_version == 1:
            URL = config.RUI1_ENDPS["IN_URL"]
        elif args.rui_version == "2":
            URL = config.RUI2_ENDPS["IN_URL"]
    elif args.server == 3:
        if args.rui_version == 1:
            URL = config.RUI1_ENDPS["EU_URL"]
        elif args.rui_version == 2:
            URL = config.RUI2_ENDPS["EU_URL"]  
  
    if args.timeout:
        TIMEOUT = args.timeout
    
    if args.rui_version == 1:
        HEADERS = config.RUI1_HEADERS
        DATA = config.RUI1_DATA
        
        DATA['otaVersion'] = OTA_VERSION
        DATA['productName'] = PRODUCT
        DATA['romVersion'] = MINOR_VERSION
        DATA['time'] = TIME
        DATA['otaPrefix'] = MINOR_VERSION

    elif args.rui_version == 2:
        HEADERS = config.RUI2_HEADERS
        DATA = config.RUI2_DATA
                
        DATA['model'] = PRODUCT
        HEADERS['model'] = PRODUCT
        HEADERS['otaVersion'] = OTA_VERSION 

    if not args.silent:
        logger.log(f"RealmeUI V{args.rui_version} {PRODUCT} ({PRODUCT_IDENTIFIER}) - {MAJOR_VERSION}")

    if args.rui_version == 1:
        try:
            response = requests.post(URL, 
                data = json.dumps({'params': crypto.encrypt_ecb(json.dumps(DATA))}), headers = HEADERS, timeout = TIMEOUT)
        except Exception as e:
            die(f"This shouldn't happen. Something went wrong while requesting to the endpoint ({e})!", -1, 3)
        
    elif args.rui_version == 2:
        try:
            response = requests.post(URL, json = {'params': crypto.encrypt_ctr(json.dumps(DATA)).decode("utf-8")}, headers = HEADERS, timeout = 30)
        except Exception as e:
            die(f"This shouldn't happen. Something went wrong while requesting to the endpoint ({e})!", -1, 3)
    
    if response.status_code != 200:
        die(f"Received invalid response: {response.status_code} :(!", -1, 2)

    if args.rui_version == 1:
        try:
            content = json.loads(crypto.decrypt_ecb(json.loads(response.content)['resps']))
        except Exception as e:
            die(f"This shouldn't happen. Something went wrong while trying to decrypt the response ({e})!", -1, 3)
        
    elif args.rui_version == 2:
        try:
            content = json.loads(crypto.decrypt_ctr(json.loads(response.content)['body']))
        except Exception as e:
            die(f"This shouldn't happen. Something went wrong while trying to decrypt the response ({e})!", -1, 3)
        
    if args.only:
        try:
            content = content[args.only]
        except Exception as e:
            die(f"Invalid response value: {args.only}!", -1, 2)

    if args.dump:
        try:
            with open(args.dump, "w") as fp:
                json.dump(content, fp, sort_keys=True, indent=4)
        except Exception as e:
            if not args.silent:
                logger.log(f"Something went wrong while writing the response to {args.dump} {e}!", 1)
        else:
            if not args.silent:
                logger.log(f"Successfully saved request as {args.dump}!")

    if not args.dump:
        print(f"{json.dumps(content, indent=4, sort_keys=True)}")

if __name__ == '__main__':
    main()
