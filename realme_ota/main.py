#!/usr/bin/python3

import requests
import json

from argparse import ArgumentParser

try:
    from utils import crypto
    from utils import data
    from utils.logger import Logger
    from utils.request import Request
except ImportError:
    from realme_ota.utils import crypto
    from realme_ota.utils import data
    from realme_ota.utils.request import Request
    from realme_ota.utils.logger import Logger

def main():
    parser = ArgumentParser()
    parser.add_argument("product_model", type=str, help="Product Model (ro.product.name).")
    parser.add_argument("ota_version", help="OTA Version (ro.build.version.ota).")
    parser.add_argument("rui_version", type=int, choices=[1, 2, 3], help="RealmeUI Version (ro.build.version.realmeui).")
    parser.add_argument("-r", "--region", type=int, choices=[0, 1, 2, 3], default=0, help="Use custom region for the request (GL = 0, CN = 1, IN = 2, EU = 3).")
    parser.add_argument("-d", "--dump", type=str, help="Save request response into a file.")
    parser.add_argument("-o", "--only", type=str, help="Only show the desired value from the response.")
    parser.add_argument("-s", "--silent", type=bool, choices=[0, 1], default=0, help="Enable silent output (purge logging).")
    parser.add_argument("-v", "--verbosity", type=int, choices=[0, 1], default=1, help="Increase or decrease logging verbosity.")
    args = parser.parse_args()

    logger = Logger(
        silent = args.silent,
        verbosity = args.verbosity
    )

    request = Request(
        model = args.product_model,
        ota_version = args.ota_version,
        rui_version = args.rui_version,
        region = args.region
    )

    logger.log(f"Load payload for {args.product_model} (RealmeUI V{args.rui_version})")
    try:
        request.set_vars()
        request.set_hdrs()
        request.set_body()
    except Exception as e:
        logger.die(f"Something went wrong while setting the request variables :( ({e})!", 2)

    logger.log("Wait for the endpoint to reply")
    try:
        if args.rui_version == 1:
            response = requests.post(data.urls[args.rui_version][args.region], data = request.body, headers = request.headers, timeout = 30)
        else:
            response = requests.post(data.urls[args.rui_version][args.region], json = request.body, headers = request.headers, timeout = 30)
    except Exception as e:
        logger.die(f"Something went wrong while requesting to the endpoint :( {e}!", 3)

    if response.status_code != 200:
        logger.die(f"Received {response.status_code} instead of the expected response :(!", 2)

    try:
        request.check_response(json.loads(response.content))
    except Exception as e:
        logger.die(f'{e}', 3)
    else:
        logger.log("All good")

    logger.log("Let's rock")
    try:
        content = json.loads(request.decrypt(json.loads(response.content)[request.resp_key]))
    except Exception as e:
        logger.die("Something went wrong while parsing the response :( {e}!", 2)
        
    if args.only:
        try:
            content = content[args.only]
        except Exception as e:
            logger.die(f"Invalid response key: {args.only}!", 2)

    if args.dump:
        try:
            with open(args.dump, "w") as fp:
                json.dump(content, fp, sort_keys=True, indent=4)
        except Exception as e:
            logger.die(f"Something went wrong while writing the response to {args.dump} {e}!", 3)
        else:
            logger.log(f"Successfully saved request as {args.dump}!")

    if not args.dump:
        print(f"{json.dumps(content, indent=4, sort_keys=True)}")

if __name__ == '__main__':
    main()