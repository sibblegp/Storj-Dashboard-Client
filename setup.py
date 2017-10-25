#!/usr/bin/env python3

from setuptools import setup

setup(name='storjdash',
      version='0.2.1',
      description='Storj Reporter',
      packages=['storjreports'],
      author='George Sibble',
      author_email='gsibble@gmail.com',
      url='https://www.gibhub.com/sibblegp/storjdash/',
      install_requires=[
            'requests==2.18.4',
            'python-crontab==2.2.5'
      ],
      entry_points={
          'console_scripts': [
              'send_storj_reports=storjreports:run_reports',
              'register_storjdash=storjreports:register'
          ],
      }
 )