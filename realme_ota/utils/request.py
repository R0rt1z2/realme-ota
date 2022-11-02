import json

try:
    from utils import data
    from utils import crypto
except ImportError:
    from realme_ota.utils import data
    from realme_ota.utils import crypto

class Request:
    def __init__(self, model=None, ota_version=None, nv_identifier=None, rui_version=None, region=None, deviceId=None, imei0=None, imei1=None, beta=False):
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
        if beta:
            self.properties['mode'] = '1'
        self.body = None
        self.headers = dict()
        self.url = None

    def encrypt(self, buf):
        return (crypto.encrypt_ecb(buf) if self.properties.get('rui_version') <= 1 \
            else crypto.encrypt_ctr(buf))

    def decrypt(self, buf):
        return (crypto.decrypt_ecb(buf) if self.properties.get('rui_version') <= 1 \
            else crypto.decrypt_ctr(buf))

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

    def set_body(self):
        new_body = dict()
        for entry in list(data.default_body.keys()):
            new_body[entry] = self.properties.get(entry) or data.default_body[entry]

        self.body = json.dumps({'params': self.encrypt(json.dumps(new_body))})
        return new_body

    def set_hdrs(self):
        for entry in list(data.default_headers.keys()):
            self.headers[entry] = self.properties.get(entry) or data.default_headers[entry]
            if entry == "deviceId":
                self.headers[entry] = crypto.sha256(self.headers[entry])
        return self.headers

    def validate_response(self, response):
        if response.status_code != 200 or 'responseCode' in json.loads(response.content) and json.loads(response.content)['responseCode'] != 200:
            if response.status_code != 200:
                raise RuntimeError(f"Response status mismatch, expected '200' got '{response.status_code}'!")
            else:
                raise RuntimeError(f"Response status mismatch, expected '200' got '{json.loads(response.content)['responseCode']}' ({json.loads(response.content)['errMsg']})!")

    def validate_content(self, content):
        if 'checkFailReason' in content and content['checkFailReason'] != None:
            raise RuntimeError(f"Response contents mismatch, expected '{self.resp_key}' got '{content['checkFailReason']}'!")
