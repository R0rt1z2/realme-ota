#!/usr/bin/python3

from distutils.core import setup

setup(name='realme-ota',
      version='2.0',
      description="CLI tool to receive requests from Realme's OTA endpoint.",
      author='Roger Ortiz',
      author_email='',
      url='https://github.com/R0rt1z2/realme-ota',
      packages=['realme_ota', 'realme_ota.utils'],
      scripts=['realme-ota']
)
