default_headers = {
    'language': 'unknown',
    'romVersion' : 'unknown',
    'otaVersion' : 'unknown',
    'androidVersion' : 'unknown',
    'colorOSVersion' : 'unknown',
    'model' : 'unknown',
    'infVersion' : '1',
    'operator' : 'unknown',
    'nvCarrier' : 'unknown',
    'uRegion' : 'unknown',
    'trackRegion' : 'unknown',
    'imei' : '000000000000000',
    'mode' : '0',
    'Accept': 'application/json',
    'User-Agent': 'NULL',
    'Content-Type' : 'application/json'
}

default_body = {
    'language': 'unknown',
    'romVersion': 'unknown',
    'otaVersion': 'unknown',
    'colorOSVersion': 'unknown',
    'androidVersion': 'unknown',
    'model': 'unknown',
    'productName': 'unknown',
    'operator': 'unknown',
    'uRegion': 'unknown',
    'trackRegion': 'unknown',
    'imei': 'unknown',
    'mode': '0',
    'registrationId': 'unknown',
    'ota_register_trigger_id': 'unknown',
    'deviceId': 'unknown',
    'version': '2',
    'type': '1',
    'otaPrefix': 'unknown',
    'isRealme': 'unknown',
    'time': '0',
    'canCheckSelf': '0'
}

urls = {
    1 : {
        0 : 'https://ifota.realmemobile.com/post/Query_Update', # GL
        1 : 'https://iota.coloros.com/post/Query_Update', # CN
        2 : 'https://ifota-in.realmemobile.com/post/Query_Update', # IN
        3 : 'https://ifota-eu.realmemobile.com/post/Query_Update' # EU
    },
    2 : {
        0 : 'https://component-ota-f.coloros.com/update/v1', # GL
        1 : 'https://component-ota.coloros.com/update/v1', # CN
        2 : 'https://component-ota-in.coloros.com/update/v1', # IN
        3 : 'https://component-ota-eu.coloros.com/update/v1' # EU
    },
    3 : {
        0 : 'https://component-ota-f.coloros.com/update/v2', # GL
        1 : 'https://component-ota.coloros.com/update/v2', # CN
        2 : 'https://component-ota-in.coloros.com/update/v2', # IN
        3 : 'https://component-ota-eu.coloros.com/update/v2' # EU
    }
}