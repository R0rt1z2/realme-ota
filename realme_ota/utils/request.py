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

import json
from time import time

try:
    from utils import data
    from utils import crypto
except ImportError:
    from realme_ota.utils import data
    from realme_ota.utils import crypto

class Request:
    def __init__(self, req_version = 1, model=None, ota_version=None, nv_identifier=None,
        rui_version=None, region=None, deviceId=None, imei0=None, imei1=None, beta=False):
        self.properties = {
            'model': model,
            'productName': model,
            'nvId': nv_identifier,
            'otaVersion': ota_version,
            'rui_version': rui_version,
            'region': region,
            'deviceId': deviceId,
            'imei': imei0,
            'imei1': imei1
        }
        self.beta = beta
        self.req_version = req_version
        if deviceId:
            self.properties['deviceId'] = crypto.sha256(deviceId)   # This is done by the OTA application on the phone
        elif imei0:
            self.properties['deviceId'] = crypto.sha256(imei0)  # This is done by the realme update tool companion app
        else:
            self.properties['deviceId'] = crypto.sha256(default_headers['deviceId'])
        if rui_version == 1:
            self.properties['version'] = '2'
        
        self.key = None
        self.body = None
        self.headers = dict()
        
        if model in ['OnePlus', 'oneplus', 'Oneplus']:
            # OnePlus uses the same server no matter what the Android Version is.
            # I'm not sure if they have more endpoints so hardcode the known URL.
            self.url = 'https://otag.h2os.com/post/Query_Update'
        elif rui_version >= 2 and req_version == 2:
            self.url = data.server_params[region]['serverURL']
        else:
            self.url = data.urls[int(rui_version)][int(region)]

    def encrypt(self, buf):
        if self.properties.get('rui_version') == 1:
            return crypto.encrypt_ecb(buf), None, None
        elif self.req_version == 2:
            return crypto.encrypt_ctr_v2(buf)
        else:
            return crypto.encrypt_ctr(buf), None, None

    def decrypt(self, buf):
        if self.properties.get('rui_version') == 1:
            return crypto.decrypt_ecb(buf)
        elif self.req_version == 2:
            body_object = json.loads(buf)
            return crypto.decrypt_ctr_v2(body_object['cipher'], self.key, body_object['iv'])
        else:
            return crypto.decrypt_ctr(buf)

    def set_vars(self):
        region = self.properties.get('region')
        rui_version = self.properties.get('rui_version')
        nvId = self.properties.get('nvId')

        #
        # @name(s): trackRegion, uRegion
        # @value(s): ro.oppo.regionmark, persist.sys.oppo.region
        #
        self.properties['trackRegion'] = self.properties['uRegion'] = 'CN' if region == 1 else 'IN' if region == 2 else 'EU' if region == 3 else 'GL'

        #
        # @name(s): language
        # @value(s): LOCALE
        #
        if region == 1:
            self.properties['language'] = 'zh-CN'

        #
        # @name(s): androidVersion
        # @value(s): Android{Version}
        #
        self.properties['androidVersion'] = 'Android' + ('10.0' if rui_version == 1 else '11.0' if rui_version == 2 else '12.0' if rui_version == 3 else '13.0')

        #
        # @name(s): colorOSVersion
        # @value(s): ColorOS{Version}
        #
        self.properties['colorOSVersion'] = 'ColorOS' + ('7' if rui_version == 1 else '11' if rui_version == 2 else '12' if rui_version == 3 else '13')

        #
        # @name(s): nvCarrer, partCarrier, localCarrier
        # @value(s): ro.build.oplus_nv_id
        #
        if nvId and nvId != '0':
            self.properties['nvCarrier'] =  self.properties['partCarrier'] = \
                self.properties['localCarrier'] = nvId
        else:
            self.properties['nvCarrier'] = self.properties['partCarrier'] = \
                self.properties['localCarrier'] = '10010111' if region == 1 else '01000100' if region == 3 else '00011011'

        #
        # @name(s): isRealme
        # @value(s): RMX -> 1
        #
        self.properties['isRealme'] = '1' if 'RMX' in self.properties.get('model') else '0'

        #
        # @name(s): romPrefix, romVersion, otaPrefix
        # @value(s): ro.build.version.ota
        #
        self.properties['romPrefix'] = self.properties['romVersion'] = \
            self.properties['otaPrefix'] = '_'.join(self.properties.get('otaVersion').split('_')[:2])

        self.resp_key = 'resps' if rui_version == 1 else 'body'
        
        self.properties['time'] = int(time() * 1000)    # Time in ms
    
    def set_body_headers(self):
        new_body = dict()
        
        for entry in list(data.default_body.keys()):
            new_body[entry] = self.properties.get(entry) or data.default_body[entry]
            if entry == 'mode' and self.beta:
                new_body[entry] = '1'
        
        for entry in list(data.default_headers.keys()):
            self.headers[entry] = self.properties.get(entry) or data.default_headers[entry]
        
        if self.req_version == 2:
            self.headers['version'] = '2'
            
            cipher, iv, self.key = self.encrypt(json.dumps(new_body))
            self.body = json.dumps({'params': json.dumps({'cipher': cipher, 'iv': iv})})
            
            region = self.properties.get('region', 0)
            protectedKey = crypto.generate_protectedKey(self.key, data.server_params[region]['pubKey'])
            negotiationVersion = data.server_params[region]['negotiationVersion']
            version = self.properties['time'] + (86400 * 1000)  # 1 day in the future
            
            self.headers['protectedKey'] = json.dumps({'SCENE_1': {'protectedKey': protectedKey,'version': version,'negotiationVersion': negotiationVersion}})
        else:
            cipher = self.encrypt(json.dumps(new_body))[0]
            self.body = json.dumps({'params': cipher})
        
        return self.body, self.headers

    def validate_response(self, response):
        if response.status_code != 200 or 'responseCode' in json.loads(response.content) and json.loads(response.content)['responseCode'] != 200:
            if response.status_code != 200:
                raise RuntimeError(f"Response status mismatch, expected '200' got '{response.status_code}'!")
            else:
                raise RuntimeError(f"Response status mismatch, expected '200' got '{json.loads(response.content)['responseCode']}' ({json.loads(response.content)['errMsg']})!")

    def validate_content(self, content):
        if 'checkFailReason' in content and content['checkFailReason'] != None:
            raise RuntimeError(f"Response contents mismatch, expected '{self.resp_key}' got '{content['checkFailReason']}'!")
