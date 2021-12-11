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
usage: main.py [-h] [-c SERVER] [-t TIMEOUT] [-d DUMP] [-o ONLY] [-s] [-v {0,1}] product_model ota_version rui_version

positional arguments:
  product_model         Product Model (ro.product.name).
  ota_version           OTA Version (ro.build.version.ota).
  rui_version           RealmeUI Version (ro.build.version.realmeui) [1,2,3].

optional arguments:
  -h, --help            show this help message and exit
  -c SERVER, --server SERVER
                        Use specific server for the request (GL = 0, CN = 1, IN = 2, EU = 3).
  -t TIMEOUT, --timeout TIMEOUT
                        Use custom timeout for the request.
  -d DUMP, --dump DUMP  Save request response into file.
  -o ONLY, --only ONLY  Only show the desired value from the request.
  -s, --silent          Enable silent output (purge logging).
  -v {0,1}, --verbosity {0,1}
                        Increase or decrease verbosity.
```

## Compatibility
The tool currently supports the following RealmeUI versions:
* RUI1 (Android 10).
* RUI2 (Android 11).
* RUI3 (Android 12) [Only IN server].

## License
* This tool is licensed under the GNU (v3) General Public License. See `LICENSE` for more details.
