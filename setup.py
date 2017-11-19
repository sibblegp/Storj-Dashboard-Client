#!/usr/bin/env python3

from setuptools import setup

VERSION = '0.3.7'

setup(name='storjdash',
      version=VERSION,
      description='Storj Reporter',
      packages=['storjreports'],
      author='George Sibble',
      author_email='gsibble@storjdash.com',
      python_requires='>=3.5',
      url='https://github.com/sibblegp/Storj-Dashboard-Client',
      install_requires=[
            'requests==2.18.4',
            'python-crontab==2.2.5'
      ],
      entry_points={
          'console_scripts': [
              'send_storj_reports=storjreports:run_reports',
              'register_storjdash=storjreports:register'
          ]
      }
 )
