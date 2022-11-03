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
usage: realme-ota [-h] [-v {0,1,2,3,4,5} | -s] [-r {0,1,2,3}] [-g GUID]
               [-i IMEI [IMEI ...]] [-b] [-d DUMP] [-o ONLY]
               product_model ota_version {1,2,3,4} [nv_identifier]

positional arguments:
  product_model         Product Model (ro.product.name).
  ota_version           OTA Version (ro.build.version.ota).
  {1,2,3,4}             RealmeUI Version (ro.build.version.realmeui).
  nv_identifier         NV (carrier) identifier (ro.build.oplus_nv_id) (if
                        none, provide 0 or omit).

optional arguments:
  -h, --help            show this help message and exit
  -v {0,1,2,3,4,5}, --verbosity {0,1,2,3,4,5}
                        Set the verbosity level. Range: 0 (no logging) to 5
                        (debug). Default: 4 (info).
  -s, --silent          Enable silent output (purge logging). Shortcut for
                        '-v0'.

request options:
  -r {0,1,2,3}, --region {0,1,2,3}
                        Use custom region for the request (GL = 0, CN = 1, IN
                        = 2, EU = 3).
  -g GUID, --guid GUID  The guid of the third line in the file
                        /data/system/openid_config.xml (only required to
                        extract 'CBT' in China).
  -i IMEI [IMEI ...], --imei IMEI [IMEI ...]
                        Specify one or two IMEIs for the request.
  -b, --beta            Try to get a test version (IMEI probably required).

output options:
  -d DUMP, --dump DUMP  Save request response into a file.
  -o ONLY, --only ONLY  Only show the desired value from the response.
```

## Additional notes
* If your request returns `flow limit` or status code `500`, try to wait a few minutes and then request again.
* Since Android 11 (RUI2), Realme started using components, which means you won't be able to get a full OTA link.
* The `--beta` option might not work correctly, it has not been fully tested!

## License
* This tool is licensed under the GNU (v3) General Public License. See `LICENSE` for more details.
