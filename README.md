# Realme OTA Downloader
![License](https://img.shields.io/github/license/R0rt1z2/realme-ota)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/R0rt1z2/realme-ota?include_prereleases)
![GitHub Issues](https://img.shields.io/github/issues-raw/R0rt1z2/realme-ota?color=red)

CLI tool (based on this [C# program](https://github.com/4j17h/realmeOTAUpdates)) to create requests to the Realme's endpoint.

## Requirements
* Python 3.9.
* pycryptodome.

## Installation
```bash
sudo apt install python3-pip
sudo pip3 install --upgrade pycryptodome git+https://github.com/R0rt1z2/realme-ota
```

## Usage
```bash
usage: realme-ota [-h] [-c SERVER] [-i IMEI] [-t TIMEOUT] [-a ANDROID] [-r ROOT] [-d DUMP] [-o ONLY] [-s] [-v {0,1}] product_model ota_version

positional arguments:
  product_model         Product Model (ro.product.name).
  ota_version           OTA Version (ro.build.version.ota).

optional arguments:
  -h, --help            show this help message and exit
  -c SERVER, --server SERVER
                        Use specific server for the request (GL = 0, CN = 1, IN = 2).
  -i IMEI, --imei IMEI  Use custom IMEI for the request.
  -t TIMEOUT, --timeout TIMEOUT
                        Use custom timeout for the request.
  -a ANDROID, --android ANDROID
                        Use custom android version for the request.
  -r ROOT, --root ROOT  Use custom root status for the request.
  -d DUMP, --dump DUMP  Save request response into file.
  -o ONLY, --only ONLY  Only show the desired value from the request.
  -s, --silent          Enable silent output (purge logging).
  -v {0,1}, --verbosity {0,1}
                        Increase or decrease verbosity.
```

## Usage example
```bash
# Normal usage - print the entire request
r0rt1z2@r0rt1z2: $ realme-ota RMX2020 RMX2020_11.A.59_0590_202102181155
[2021-09-23 20:26:38.037321] I: Requesting for RMX2020 - RMX2020_11.A.59...
[2021-09-23 20:26:38.764134] I: {'parent': 'ota', 'otaVersion': 'RMX2020_11.A.65_0650_202108211659', 'down_url': 'https://ota-manual-sg.allawnofs.com/ota/21/08/24/5a398f51-8900-4178-8153-60b98bf4bf7e.ozip', 'newAndroidVersion': 'Android 10', 'description': 'http://ota-manual-sg.allawnofs.com/ota/21/08/30/69f5202e26b14b789054d9b9ac4cc9d8.html', 'recommend': '100', 'language': 'en-IN', 'versionName': 'RMX2020_11_A.65', 'rid': '96d9b7df-092a-4ac1-b810-b8a5664e7745', 'type': '1', 'newColorOSVersion': 'ColorOS 7.0', 'patch_size': '3287752078', 'patchFilePath': '/patch/amazone2/GLO/RMX2020/RMX2020_11.A.65_0650_202108211659/RMX2020_11_OTA_0650_all_xokQsbsYqeC2.ozip', 'osVersion': 'ColorOS 7.0', 'share': '.', 'id': '61330f13f69bc3c9e42fd3a3', 'googlePatchLevel': '0', 'patch_name': 'RMX2020_11_OTA_0650_all_xokQsbsYqeC2.ozip', 'paramFlag': 1, 'needDataSpace': '0', 'noticeType': 0, 'new_version': 'RMX2020_11.A.65_0650_202108211659', 'patch_md5': 'd99b0ea8069f9bd3b7c00296b01dc372', 'versionCode': 650, 'silenceUpdate': 0, 'active_url': 'https://ota-manual-sg.allawnofs.com/ota/21/08/24/5a398f51-8900-4178-8153-60b98bf4bf7e.ozip', 'wipe': '0', 'questionnaireEnable': False, 'extract': 'This release updated Android security patch and improved system stability.', 'version_name': 'RMX2020_11_A.65', 'aid': 'RMX2020_11.A', 'status': 'published', 'msg': 'SUCCEED', 'resultCode': 1}
r0rt1z2@r0rt1z2: $
```

```bash
# Custom usage - only print the download URL
r0rt1z2@r0rt1z2: $ realme-ota RMX2020 RMX2020_11.A.59_0590_202102181155 -o down_url -s -v 0
https://ota-manual-sg.allawnofs.com/ota/21/08/24/5a398f51-8900-4178-8153-60b98bf4bf7e.ozip
r0rt1z2@r0rt1z2: $
```

## License
* This tool is licensed under the GNU (v3) General Public License. See `LICENSE` for more details.
