RUI1_ENDPS = {
    'GL_URL' : 'https://ifota.realmemobile.com/post/Query_Update',
    'IN_URL' : 'https://ifota-in.realmemobile.com/post/Query_Update',
    'EU_URL' : 'https://ifota-eu.realmemobile.com/post/Query_Update',
    'CN_URL' : 'https://iota.coloros.com/post/Query_Update'
}

RUI2_ENDPS = {
    'GL_URL' : 'https://component-ota-f.coloros.com/update/v1',
    'IN_URL' : 'https://component-ota-in.coloros.com/update/v1',
    'EU_URL' : 'https://component-ota-eu.coloros.com/update/v1',
    'CN_URL' : 'https://component-ota-cn.coloros.com/update/v1'
}

RUI3_ENDPS = {
    'IN_URL' : 'https://component-ota-in.allawnos.com/update/v2'
}

TIMEOUT = 30

RUI1_HEADERS = {
    'Accept': 'application/json',
    'User-Agent': 'NULL',
    'Content-Type' : 'application/json'
}

RUI2_HEADERS = {
    'language': 'en',
    'romVersion': 'V1.0.0',
    'androidVersion': 'Android 11.0',
    'colorOSVersion': 'ColorOS V11',
    'infVersion': '1',
    'operator': 'UNKNOWN',
    'otaVersion': 'NULL',
    'trackRegion': 'UNKNOWN',
    'uRegion': 'UNKNOWN',
    'model': 'NULL',
    'nvCarrier': '00011011',
    'imei': '000000000000000',
    'mode': '1'
}

RUI3_HEADERS = {
    'language': 'en',
    'romVersion': 'V1.0.0',
    'androidVersion': 'Android 12.0',
    'colorOSVersion': 'ColorOS V12',
    'infVersion': '1',
    'operator': 'UNKNOWN',
    'otaVersion': 'NULL',
    'trackRegion': 'UNKNOWN',
    'uRegion': 'UNKNOWN',
    'model': 'NULL',
    'nvCarrier': '00011011',
    'imei': '000000000000000',
    'mode': '1'
}

RUI1_DATA = {
    'version': '2',
    'otaVersion': 'NULL',
    'imei': 'NULL',
    'mode': '0',
    'language': 'en',
    'productName': 'NULL',
    'type': '1',
    'romVersion': 'NULL',
    'colorOSVersion': 'UNKNOWN',
    'androidVersion': '10',
    'time': 'NULL',
    'registrationId': 'UNKNOWN',
    'operator': 'UNKNOWN',
    'trackRegion': 'UNKNOWN',
    'ota_register_trigger_id': 'UNKNOWN',
    'uRegion': 'UNKNOWN',
    'isRooted': '0',
    'isRealme': '1',
    'canCheckSelf': '0',
    'otaPrefix': 'NULL',
    'secret': 'a1b2c3d5e'
}

RUI2_DATA = {
    'forbiddenUpdate': '0',
    'isRooted': '1',
    'type': '2',
    'registrationId': 'UNKNOWN',
    'securityPatch': 'UNKNOWN',
    'securityPatchVendor': 'UNKNOWN',
    'deviceId': 'UNKNOWN',
    'model': 'UNKNOWN',
    'androidVersion': '11.0',
}

RUI3_DATA = {
    'forbiddenUpdate': '0',
    'isRooted': '1',
    'type': '2',
    'registrationId': 'UNKNOWN',
    'securityPatch': 'UNKNOWN',
    'securityPatchVendor': 'UNKNOWN',
    'deviceId': 'UNKNOWN',
    'model': 'UNKNOWN',
    'androidVersion': '12.0',
}