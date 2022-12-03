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
#!/usr/bin/python3

import os
import sys
import json
import requests

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
    # Verbosity
    verbosity = parser.add_mutually_exclusive_group()
    verbosity.add_argument("-v", "--verbosity", type=int, choices=range(0, 6), default=4, help="Set the verbosity level. Range: 0 (no logging) to 5 (debug). Default: 4 (info).")
    verbosity.add_argument("-s", "--silent", action='store_true', help="Enable silent output (purge logging). Shortcut for '-v0'.")
    # Positional arguments
    parser.add_argument("product_model", type=str, help="Product Model (ro.product.name).")
    parser.add_argument("ota_version", help="OTA Version (ro.build.version.ota).")
    parser.add_argument("rui_version", type=int, choices=[1, 2, 3, 4], help="RealmeUI Version (ro.build.version.realmeui).")
    parser.add_argument("nv_identifier", type=str, nargs='?', help="NV (carrier) identifier (ro.build.oplus_nv_id) (if none, provide 0 or omit).")
    # Request attributes
    req_opts = parser.add_argument_group("request options")
    req_opts.add_argument("-r", "--region", type=int, choices=[0, 1, 2, 3], default=0, help="Use custom region for the request (GL = 0, CN = 1, IN = 2, EU = 3).")
    req_opts.add_argument("-g", "--guid", type=str, default="0", help="The guid of the third line in the file /data/system/openid_config.xml (only required to extract 'CBT' in China).")
    req_opts.add_argument("-i", "--imei", type=str, nargs='+', help="Specify one or two IMEIs for the request.")
    req_opts.add_argument("-b", "--beta", action='store_true', help="Try to get a test version (IMEI probably required).")
    # Output settings
    out_opts = parser.add_argument_group("output options")
    out_opts.add_argument("-d", "--dump", type=str, help="Save request response into a file.")
    out_opts.add_argument("-o", "--only", type=str, help="Only show the desired value from the response.")
    
    args = parser.parse_args()

    logger = Logger(
        level = 0 if args.silent else args.verbosity
    )

    request = Request(
        model = args.product_model,
        ota_version = args.ota_version,
        rui_version = args.rui_version,
        nv_identifier = args.nv_identifier,
        region = args.region,
        deviceId = args.guid,
        imei0 = args.imei[0] if args.imei and len(args.imei) > 0 else None,
        imei1 = args.imei[1] if args.imei and len(args.imei) > 1 else None,
        beta = args.beta
    )

    logger.log(f"Load payload for {args.product_model} (RealmeUI V{args.rui_version})")
    try:
        request.set_vars()
        req_hdrs = request.set_hdrs()
        req_body = request.set_body()
    except Exception as e:
        logger.die(f"Something went wrong while setting the request variables :( ({e})!", 2)
    
    logger.log(f"Request headers:\n{json.dumps(req_hdrs, indent=4, sort_keys=True)}", 5)
    logger.log(f"Request body:\n{json.dumps(req_body, indent=4, sort_keys=True)}", 5)
    
    logger.log("Wait for the endpoint to reply")
    try:
        response = requests.post(request.url, data = request.body, headers = request.headers, timeout = 30)
    except Exception as e:
        logger.die(f"Something went wrong while requesting to the endpoint :( {e}!", 1)

    try:
        request.validate_response(response)
    except Exception as e:
        if args.ota_version[-17:] != '0000_000000000000':
            sys.argv[sys.argv.index(args.ota_version)] = args.ota_version[:-17] + '0000_000000000000'
            os.execl(sys.executable, sys.executable, *sys.argv)
        logger.die(f'{e}', 1)
    else:
        logger.log("All good")

    logger.log("Let's rock")
    try:
        content = json.loads(request.decrypt(json.loads(response.content)[request.resp_key]))
    except Exception as e:
        logger.die(f"Something went wrong while parsing the response :( {e}!", 2)

    try:
        request.validate_content(content)
    except Exception as e:
        logger.die(f'{e}', 1)
    else:
        logger.log("Party time")

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
            logger.die(f"Something went wrong while writing the response to {args.dump} {e}!", 1)
        else:
            logger.log(f"Successfully saved request as {args.dump}!")
    else:
        print(f"{json.dumps(content, indent=4, sort_keys=True)}")

if __name__ == '__main__':
    main()
