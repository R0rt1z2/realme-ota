default_headers = {
    'deviceId'       : '0',          # N/A
    'language'       : 'en-EN',            # lang-LANG
    'romVersion'     : 'unknown',          # ro.build.version.ota
    'otaVersion'     : 'unknown',          # ro.build.version.ota
    'androidVersion' : 'unknown',          # Android{Version}
    'colorOSVersion' : 'unknown',          # ColorOS{Version}
    'model'          : 'unknown',          # ro.product.name
    'infVersion'     : '1',                # N/A
    'operator'       : 'unknown',          # ro.product.name
    'nvCarrier'      : 'unknown',          # ro.build.oplus_nv_id
    'uRegion'        : 'unknown',          # persist.sys.oppo.region (RUI1)
    'trackRegion'    : 'unknown',          # ro.oppo.regionmark (RUI1)
    'imei'           : '000000000000000',  # IMEI
    'mode'           : '0',                # N/A
    'Accept'         : 'application/json', # N/A
    'Content-Type'   : 'application/json', # N/A
    'User-Agent'     : 'NULL'              # N/A
}

default_body = {
    'deviceId'       : '0',          # N/A
    'language'       : 'en-EN',            # lang-LANG
    'romVersion'     : 'unknown',          # ro.build.version.ota
    'otaVersion'     : 'unknown',          # ro.build.version.ota
    'androidVersion' : 'unknown',          # Android{Version}
    'colorOSVersion' : 'unknown',          # ColorOS{Version}
    'model'          : 'unknown',          # ro.product.name
    'productName'    : 'unknown',          # ro.product.name
    'operator'       : 'unknown',          # ro.product.name
    'uRegion'        : 'unknown',          # persist.sys.oppo.region (RUI1)
    'trackRegion'    : 'unknown',          # ro.oppo.regionmark (RUI1)
    'imei'           : '000000000000000',  # IMEI
    'mode'           : '0',                # N/A
    'registrationId' : 'unknown',          # N/A
    'version'        : '3',                # N/A
    'type'           : '1',                # N/A
    'otaPrefix'      : 'unknown',          # ro.build.version.ota
    'isRealme'       : 'unknown',          # N/A
    'time'           : '0',                # N/A
    'canCheckSelf'   : '0'                 # N/A
}

urls = {
    1 : {
        0 : 'https://ifota.realmemobile.com/post/Query_Update',    # GL
        1 : 'https://iota.coloros.com/post/Query_Update',          # CN
        2 : 'https://ifota-in.realmemobile.com/post/Query_Update', # IN
        3 : 'https://ifota-eu.realmemobile.com/post/Query_Update'  # EU
    },
    2 : {
        0 : 'https://component-ota-f.coloros.com/update/v1',       # GL
        1 : 'https://component-ota.coloros.com/update/v1',         # CN
        2 : 'https://component-ota-in.coloros.com/update/v1',      # IN
        3 : 'https://component-ota-eu.coloros.com/update/v1'       # EU
    },
    3 : {
        0 : 'https://component-ota-f.coloros.com/update/v2',       # GL
        1 : 'https://component-ota.coloros.com/update/v2',         # CN
        2 : 'https://component-ota-in.coloros.com/update/v2',      # IN
        3 : 'https://component-ota-eu.coloros.com/update/v2'       # EU
    },
    4 : {
        0 : 'https://component-ota-f.coloros.com/update/v2',       # GL
        1 : 'https://component-ota.coloros.com/update/v2',         # CN
        2 : 'https://component-ota-in.coloros.com/update/v2',      # IN
        3 : 'https://component-ota-eu.coloros.com/update/v2'       # EU
    }
}
