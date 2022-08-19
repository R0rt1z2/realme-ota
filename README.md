# Realme OTA Downloader
![License](https://img.shields.io/github/license/R0rt1z2/realme-ota)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/R0rt1z2/realme-ota?include_prereleases)
![GitHub Issues](https://img.shields.io/github/issues-raw/R0rt1z2/realme-ota?color=red)

## Requirements
* Python 3.9.
* pycryptodome.

## Installation
```bash
sudo apt install python3-pip
pip3 install --upgrade requests pycryptodome git+https://github.com/R0rt1z2/realme-ota
```

## Usage
```bash
usage: realme-ota [-h] [-r {0,1,2,3}] [-d DUMP] [-o ONLY] [-s {0,1}] [-v {0,1}] product_model ota_version {1,2,3} nv_identifier

positional arguments:
  product_model         Product Model (ro.product.name).
  ota_version           OTA Version (ro.build.version.ota).
  {1,2,3}               RealmeUI Version (ro.build.version.realmeui).
  nv_identifier         NV (carrier) identifier (ro.build.oplus_nv_id) (if none, provide 0).

optional arguments:
  -h, --help            show this help message and exit
  -r {0,1,2,3}, --region {0,1,2,3}
                        Use custom region for the request (GL = 0, CN = 1, IN = 2, EU = 3).
  -d DUMP, --dump DUMP  Save request response into a file.
  -o ONLY, --only ONLY  Only show the desired value from the response.
  -s {0,1}, --silent {0,1}
                        Enable silent output (purge logging).
  -v {0,1}, --verbosity {0,1}
                        Increase or decrease logging verbosity.
```

## Compatibility
The tool currently supports the following RealmeUI versions:
* Realme UI 1 (Android 10).
* Realme UI 2 (Android 11).
* Realme UI 3 (Android 12).

## Additional notes
* If your request returns `flow limit` or status code `500`, try to wait a few minutes and then request again.
* Since Android 11 (RUI2), Realme started using components, which means you won't be able to get a full OTA link.

## License
* This tool is licensed under the GNU (v3) General Public License. See `LICENSE` for more details.
