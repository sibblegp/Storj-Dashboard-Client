#!/usr/bin/env python

import requests
import os
import getpass
import json
import subprocess
from random import randint

from crontab import CronTab


from os import scandir

STORJSHAREPATH = None

def gather_information():
    if os.geteuid() != 0:
        print('This script must be run with root privileges')
        exit()
    print('Storj Dashboard Registration')
    if os.path.isfile('/etc/storjdash.json'):
        print('This server has already been configured')
        exit(1)

    find_storjshare()

    if STORJSHAREPATH is None:
        print('Unable to find storjshare.  Aborting.')
        exit(1)

    print('Use this tool once and only once to register your server with StorJ Dashboard')
    user_email = input('Please enter your StorJ Dashboard account email address (If you do not have an account, please register at www.storjdash.com): ')
    password = getpass.getpass('Please enter your StorJ Dashboard password: ')
    verified = verify_user(email=user_email, password=password)

    if verified == False:
        print('Invalid user')
        exit(1)

    server_name = input('What is the name of this server: ')
    configs_directory = input('(VERY IMPORTANT) What directory holds your StorJ Configuration files: ')

    server_uuid = register_server(email=user_email, password=password, server_name=server_name)

    create_settings_file(server_uuid=server_uuid, configs_directory=configs_directory)
    create_cron_job()

    print('Your server has been registered and you should start seeing data reported on www.storjdash.com within the hour')
    exit()

def verify_user(email, password):
    json_request = {
        'email': email,
        'password': password
    }
    resp = requests.post('https://www.storjdash.com/api/users/verify/', json=json_request)
    if resp.status_code == 200:
        return True
    else:
        return False

def register_server(email, password, server_name):
    json_request = {
        'email': email,
        'password': password,
        'server_name': server_name
    }
    resp = requests.post('https://www.storjdash.com/api/servers/', json=json_request)
    if resp.status_code == 200:
        return resp.json()['server_uuid']
    else:
        print('Error registering server')
        exit(1)

def find_storjshare():
    user_directories = scandir('/home')
    for directory in user_directories:
        if directory.is_dir():
            look_for_storj(directory.path)
    if STORJSHAREPATH == None:
        look_for_storj('/usr/local/bin')


def look_for_storj(directory):
    global STORJSHAREPATH
    details = scandir(directory)
    for item in details:
        if item.is_dir():
            look_for_storj(item.path)
        else:
            if item.name == 'storjshare':
                #print('Found!')
                #print(item.path)
                #print(type(item.path))
                STORJSHAREPATH = item.path.split('storjshare')[0][:-1]
                #print(STORJSHAREPATH)

def create_settings_file(server_uuid, configs_directory):
    settings = {
        'server_uuid': server_uuid,
        'storjshare_path': STORJSHAREPATH,
        'configs_directory': configs_directory
    }

    settings_output = json.dumps(settings, sort_keys=True, indent=4)
    settings_file_path = '/etc/storjdash.json'
    settings_file = open(settings_file_path, 'w')
    settings_file.write(settings_output)
    settings_file.close()

def create_cron_job():
    env = os.environ
    env['PATH'] = env.get('PATH') + ':/usr/local/bin'
    proc = subprocess.Popen(['which', 'send_storj_reports'], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    results = proc.communicate()
    if '/' in results[0].decode('utf-8'):
        system_cron = CronTab(tabfile='/etc/crontab', user=False)
        job = system_cron.new(command=results[0].decode('utf-8') + ' >>/var/log/storj_reports.log 2>&1', user='root')
        minute = randint(0, 59)
        job.minute.on(minute)
        try:
            system_cron.write()
            update_proc = subprocess.Popen(['service', 'cron', 'reload'])
            results = update_proc.communicate()
        except PermissionError:
            print('Unable to create cron job.  Exiting.')
            exit(1)
    else:
        print('Unable to find report script.  Exiting.')
        exit(1)

if __name__ == '__main__':
    gather_information()