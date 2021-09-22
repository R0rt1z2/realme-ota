# Realme OTA Downloader
![License](https://img.shields.io/github/license/R0rt1z2/realme-ota-dl)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/R0rt1z2/realme-ota-dl?include_prereleases)
![GitHub Issues](https://img.shields.io/github/issues-raw/R0rt1z2/realme-ota-dl?color=red)

Simple Python(3) script (based on this [C# program](https://github.com/4j17h/realmeOTAUpdates)) to download OTA packages (ozips in this case) from Realme's endpoint.

## Requirements
* Python 3.9 (with pycrypto - `pip3 install -r requirement.txt`).

## Usage
```bash
realme-ota.py ro.product.name ro.build.version.ota
```

## Usage example
```bash
r0rt1z2@r0rt1z2 $ python3 realme-ota.py RMX2020 RMX2020_11.A.59_0590_202102181155
[2021-09-22 22:11:38.133028] I: Device: RMX2020
[2021-09-22 22:11:38.133918] I: Version: RMX2020_11.A.59_0590_202102181155
[2021-09-22 22:11:38.133918] I: Product identifier: A
[2021-09-22 22:11:38.852818] I: Using 20odiuye#AlW!Kc6 to decrypt the response...
[2021-09-22 22:11:38.853819] I: "{\"parent\":\"ota\",\"otaVersion\":\"RMX2020_11.A.65_0650_202108211659\",\"down_url\":\"https://ota-manual-sg.allawnofs.com/ota/21/08/24/5a398f51-8900-4178-8153-60b98bf4bf7e.ozip\",\"newAndroidVersion\":\"Android 10\",\"description\":\"https://ota-manual-sg.allawnofs.com/ota/21/08/30/aafb0a81bebc4e668e2ad0630356cded.html\",\"recommend\":\"100\",\"language\":\"en-US\",\"versionName\":\"RMX2020_11_A.65\",\"rid\":\"96d9b7df-092a-4ac1-b810-b8a5664e7745\",\"type\":\"1\",\"newColorOSVersion\":\"ColorOS 7.0\",\"patch_size\":\"3287752078\",\"patchFilePath\":\"/patch/amazone2/GLO/RMX2020/RMX2020_11.A.65_0650_202108211659/RMX2020_11_OTA_0650_all_xokQsbsYqeC2.ozip\",\"osVersion\":\"ColorOS 7.0\",\"share\":\".\",\"id\":\"61330f13f69bc3c9e42fd3a3\",\"googlePatchLevel\":\"0\",\"patch_name\":\"RMX2020_11_OTA_0650_all_xokQsbsYqeC2.ozip\",\"paramFlag\":1,\"needDataSpace\":\"0\",\"noticeType\":0,\"new_version\":\"RMX2020_11.A.65_0650_202108211659\",\"patch_md5\":\"d99b0ea8069f9bd3b7c00296b01dc372\",\"versionCode\":650,\"silenceUpdate\":0,\"active_url\":\"https://ota-manual-sg.allawnofs.com/ota/21/08/24/5a398f51-8900-4178-8153-60b98bf4bf7e.ozip\",\"wipe\":\"0\",\"questionnaireEnable\":false,\"extract\":\"This release updated Android security patch and improved system stability.\",\"version_name\":\"RMX2020_11_A.65\",\"aid\":\"RMX2020_11.A\",\"status\":\"published\",\"msg\":\"SUCCEED\",\"resultCode\":1}"
```

## License
* This tool is licensed under the GNU (v3) General Public License. See `LICENSE` for more details.