import json

try:
    from utils import data
    from utils import crypto
except ImportError:
    from realme_ota.utils import data
    from realme_ota.utils import crypto

class Request:
    body = None
    headers = None
    url = None

    def __init__(self, model : str, ota_version : str, rui_version : int, region : int):
        self.model, self.productName, self.otaVersion, self.rui_version, self.region = model, model, ota_version, rui_version, region
    
    def encrypt(self, buf):
        return (crypto.encrypt_ecb(buf) if self.rui_version <= 1 else crypto.encrypt_ctr(buf))

    def decrypt(self, buf):
        return (crypto.decrypt_ecb(buf) if self.rui_version <= 1 else crypto.decrypt_ctr(buf))
    
    def set_vars(self):
        # Region
        sregion = {self.region == 1: 'CN', 
            self.region == 2: 'IN'}.get(True, 'GL')
        self.trackRegion, self.uRegion = sregion, sregion

        # Language (en-EN, zh-CN)
        self.language = 'zh-CN' if self.region == 1 else 'en-EN'

        # Android Version (10, 11, 12)
        self.androidVersion = {self.rui_version == 1: '10.0', 
            self.rui_version == 2: '11.0'}.get(True, '12.0')
        
        # ColorOS Version (7, 11, 12)
        self.colorOSVersion = {self.rui_version == 1: '7', 
            self.rui_version == 2: '11'}.get(True, '12')
        
        # Carrier (10010111, 00011011)
        carrier = '10010111' if self.region == 1 else '00011011'
        self.nvCarrier, self.partCarrier, self.localCarrier = carrier, carrier, carrier

        # Model prefix (CPH, RMX)
        self.isRealme = '1' if 'RMX' in self.model else '0'

        # ROM Version Prefix
        self.romPrefix = self.otaVersion[:15]
        self.romVersion, self.otaPrefix = self.romPrefix, self.romPrefix

        # Response Key
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
                exec(f"data.default_headers[\"{entry}\"] = self.{entry}")
            except Exception:
                pass
        
        self.headers = data.default_headers
    
    def check_response(self, response):
        if 'errMsg' in response and response['errMsg'] != None:
            raise RuntimeError(f"Received invalid response ({response['errMsg']})!")