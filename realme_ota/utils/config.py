# Realme endpoints
GL_URL = "https://ifota.realmemobile.com/post/Query_Update"
CN_URL = "https://iota.coloros.com/post/Query_Update"
IN_URL = "https://ifota-in.realmemobile.com/Query_Update"
EU_URL= "https://ifota-eu.realmemobile.com/post/Query_Update"

# Default timeout for requests
TIMEOUT = 30

# Default headers for the requests.
HEADERS = {'Accept': 'application/json', 'User-Agent': 'NULL', 'Content-Type' : 'application/json'}

# Default body for the request
BODY = {
    "version": "2",
    "otaVersion": "NULL",
    "imei": "NULL",
    "mode": "0",
    "language": "en",
    "productName": "NULL",
    "type": "1",
    "romVersion": "NULL",
    "colorOSVersion": "UNKNOWN",
    "androidVersion": "10",
    "time": "NULL",
    "registrationId": "UNKNOWN",
    "operator": "UNKNOWN",
    "trackRegion": "UNKNOWN",
    "ota_register_trigger_id": "UNKNOWN",
    "uRegion": "UNKNOWN",
    "isRooted": "0",
    "isRealme": "1",
    "canCheckSelf": "0",
    "otaPrefix": "NULL"
}