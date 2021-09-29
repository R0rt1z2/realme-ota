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
    parser.add_argument("product_model", help="Product Model (ro.product.name).")
    parser.add_argument("ota_version", help="OTA Version (ro.build.version.ota).")
    parser.add_argument("-c", "--server", type=int, default=0, help="Use specific server for the request (GL = 0, CN = 1, IN = 2).")
    parser.add_argument("-i", "--imei", type=int, help="Use custom IMEI for the request.")
    parser.add_argument("-t", "--timeout", type=int, help="Use custom timeout for the request.")
    parser.add_argument("-a", "--android", type=str, help="Use custom android version for the request.")
    parser.add_argument("-r", "--root", type=str, help="Use custom root status for the request.")
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
    DATA = config.BODY
    URL = config.GL_URL
    TIMEOUT = config.TIMEOUT
    
    if args.server == 1:
        URL = config.CN_URL
    if args.server ==2:
        URL = config.IN_URL
    if args.timeout:
        TIMEOUT = args.timeout
    
    DATA['otaVersion'] = OTA_VERSION
    DATA['imei'] = 000000000000000
    DATA['productName'] = PRODUCT
    DATA['romVersion'] = MINOR_VERSION
    DATA['time'] = TIME
    DATA['otaPrefix'] = MINOR_VERSION

    if args.imei:
        DATA['imei'] = args.imei
    if args.android:
        DATA['androidVersion'] = args.android
    if args.root:
        DATA['isRooted'] = args.root

    if not args.silent:
        logger.log(f"Requesting for {PRODUCT} - {MINOR_VERSION}...")

    try:
        response = requests.post(URL, 
            data = json.dumps(crypto.encReq(json.dumps(DATA))), headers = config.HEADERS, timeout = TIMEOUT)
    except Exception as e:
        die(f"This shouldn't happen. Something went wrong while requesting to the endpoint ({e})!", -1, 3)
    
    if response.status_code != 200:
        die(f"Received invalid response: {response.status_code} :(!", -1, 2)

    try:
        content = crypto.decReq(json.loads(response.content)['resps'])
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
                logger.log(f"Something went wrong while writing the response to {args.dump}!", 1)
        else:
            if not args.silent:
                logger.log(f"Successfully saved request as {args.dump}!")

    logger.log(f"{content}")

if __name__ == '__main__':
    main()
