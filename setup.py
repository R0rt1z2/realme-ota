#!/usr/bin/python3

from distutils.core import setup

setup(name='realme-ota',
      version='4.0',
      description="CLI tool to receive requests from Realme's OTA endpoint.",
      author='Roger Ortiz',
      author_email='',
      install_requires=['requests', 'pycryptodome']
      packages=['realme_ota', 'realme_ota.utils'],
      scripts=['realme-ota']
)
