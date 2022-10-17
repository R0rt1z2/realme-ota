import json

try:
    from utils import data
    from utils import crypto
except ImportError:
    from realme_ota.utils import data
    from realme_ota.utils import crypto

class Request:
    def __init__(self, model, ota_version, nv_identifier, rui_version, deviceId, region):
        self.model = model
        self.productName = model
        self.nvId = nv_identifier
        self.otaVersion = ota_version
        self.rui_version = rui_version
        self.region = region
        self.deviceId = deviceId
        self.body = None
        self.headers = None
        self.url = None

    def encrypt(self, buf):
        return (crypto.encrypt_ecb(buf) if self.rui_version <= 1 \
            else crypto.encrypt_ctr(buf))

    def decrypt(self, buf):
        return (crypto.decrypt_ecb(buf) if self.rui_version <= 1 \
            else crypto.decrypt_ctr(buf))

    def set_vars(self):
        #
        # @name(s): trackRegion, uRegion
        # @value(s): ro.oppo.regionmark, persist.sys.oppo.region
        #
        self.trackRegion = self.uRegion = {self.region == 1: 'CN',
            self.region == 2: 'IN'}.get(True, 'GL')

        #
        # @name(s): language
        # @value(s): LOCALE
        #
        if self.region == 1:
            self.language = 'zh-CN'

        #
        # @name(s): androidVersion
        # @value(s): Android{Version}
        #
        self.androidVersion = 'Android' + {self.rui_version == 1: '10.0',
            self.rui_version == 2: '11.0'}.get(True, '12.0')

        #
        # @name(s): colorOSVersion
        # @value(s): ColorOS{Version}
        #
        self.colorOSVersion = 'ColorOS' + {self.rui_version == 1: '7',
            self.rui_version == 2: '11'}.get(True, '12')

        #
        # @name(s): nvCarrer, partCarrier, localCarrier
        # @value(s): ro.build.oplus_nv_id
        #
        if self.nvId != '0':
            self.nvCarrier = self.partCarrier = self.localCarrier = self.nvId
        else:
            self.nvCarrier = self.partCarrier = self.localCarrier = \
                '10010111' if self.region == 1 else '00011011'

        #
        # @name(s): isRealme
        # @value(s): RMX -> 1
        #
        self.isRealme = '1' if 'RMX' in self.model else '0'

        #
        # @name(s): romPrefix, romVersion, otaPrefix
        # @value(s): ro.build.version.ota
        #
        self.romPrefix = self.romVersion = \
            self.otaPrefix = f'{self.otaVersion.split("_")[0]}_{self.otaVersion.split("_")[1]}'

        self.resp_key = 'resps' if self.rui_version == 1 else 'body'

    def set_body(self):
        for entry in list(data.default_body.keys()):
            try:
                exec(f"data.default_body[\"{entry}\"] = self.{entry}")
            except Exception:
                pass

        if self.rui_version > 1:
            self.body = {'params': self.encrypt(json.dumps(data.default_body)).decode("utf-8")}
        else:
            self.body = json.dumps({'params': self.encrypt(json.dumps(data.default_body))})

    def set_hdrs(self):
        for entry in list(data.default_headers.keys()):
            try:
                if entry == "deviceId":
                    exec(f"data.default_headers[\"{entry}\"] = {crypto.sha256(self.deviceId)}")
                else:
                    exec(f"data.default_headers[\"{entry}\"] = self.{entry}")
            except Exception:
                pass

        self.headers = data.default_headers

    def validate_response(self, response):
        if response.status_code != 200 or 'responseCode' in json.loads(response.content) and json.loads(response.content)['responseCode'] != 200:
            if response.status_code != 200:
                raise RuntimeError(f"Response status mismatch, expected '200' got '{response.status_code}'!")
            else:
                raise RuntimeError(f"Response status mismatch, expected '200' got '{json.loads(response.content)['responseCode']}' ({json.loads(response.content)['errMsg']})!")

    def validate_content(self, content):
        if 'checkFailReason' in content and content['checkFailReason'] != None:
            raise RuntimeError(f"Response contents mismatch, expected '{self.resp_key}' got '{content['checkFailReason']}'!")