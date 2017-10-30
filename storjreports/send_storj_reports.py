#!/usr/bin/env python3

import requests
import json
import os
import re
import uuid
import subprocess


from os import scandir

SERVER_UUID = None
STORJSHARE_PATH = None

def examine_configs(path):
    storj_node_pairs = examine_storjstatus()
    #storj_node_pairs = None
    #print(storj_node_pairs)
    report_uuid = str(uuid.uuid4())
    config_files = os.scandir(path)
    for config_file in config_files:
        if config_file.is_file():
            send_report(config_file, report_uuid, storj_node_pairs)
    print('All reports sent')

def get_size_of_path(path):
    try:
        details = scandir(path)
    except FileNotFoundError:
        print('Path does not exist: ' + path)
        return 0
    size = 0
    for item in details:
        if item.is_dir():
            size += get_size_of_path(item.path)
        else:
            try:
                size += item.stat().st_size
            except FileNotFoundError:
                pass
    return size

def examine_storjstatus():
    env = os.environ
    env['PATH'] = os.environ.get('PATH') + ':' + STORJSHARE_PATH
    proc = subprocess.Popen(['storjshare', 'status'], env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    results = proc.communicate()
    #print(results)
    cells = results[0].split(b'\xe2')
    #print(cells)
    node_pairs = {}
    for index, cell in enumerate(cells):
        if '/' in str(cell):
            #print(cells[index-15:index+1])
            node_id = None

            if 'running' in str(cells[index-12]):
                node_id = cells[index-13].split(b'\x94\x82')[1]
            else:
                node_id = cells[index-12].split(b'\x94\x82')[1]
            node_path = cells[index].split(b'\x86\x92')[1]
            node_id = node_id.strip().decode('utf-8')
            node_path = node_path.strip().decode('utf-8')
            node_pairs[node_path] = node_id
    return node_pairs

def send_report(config_file, report_uuid, storj_node_pairs):
    node_name = config_file.name.split('.')[0]
    try:
        open_config_file = open(config_file.path, 'r', encoding='utf-8')
        config_contents = open_config_file.read()
    except UnicodeDecodeError:
        try:
            open_config_file = open(config_file.path, 'r', encoding='latin-1')
            config_contents = open_config_file.read()
        except UnicodeDecodeError:
            try:
                open_config_file = open(config_file.path, 'r')
                config_contents = open_config_file.read()
            except UnicodeDecodeError:
                print('Unable to read config file: ' + config_file.path)
                return

    config_contents = re.sub(r'\\\n', '', config_contents)
    regexed_config = ''
    for line in config_contents.split('\n'):
        if 'https' not in line:
            regexed_config += (re.sub(r'//.*', '', line) + '\n')
    #print(regexed_config)
    try:
        json_config = json.loads(regexed_config)
    except json.JSONDecodeError:
        try:
            config_contents = re.sub(r'https.*\n', '"', regexed_config)
            json_config = json.loads(regexed_config)
        except json.JSONDecodeError:
            print('Unable to decode JSON file: ' + config_file.name)
            return False

    try:
        storage_path = json_config['storagePath']
        capacity_line = json_config['storageAllocation']
    except KeyError:
        print('Missing Keys in Config File')
        return False
    current_size = get_size_of_path(storage_path)
    if 'GB' in capacity_line:
        capacity_gb = float(capacity_line.split('GB')[0])
        capacity = capacity_gb * 1000 * 1000000
    elif 'TB' in capacity_line:
        capacity_gb = float(capacity_line.split('TB')[0])
        capacity = float(capacity_gb * 1000 * 1000 * 1000000)
    else:
        capacity = float(capacity_line.split('B')[0])

    report_json = {
        'server_uuid': SERVER_UUID,
        'report_uuid': report_uuid,
        'node_name': node_name,
        'current_size': current_size,
        'node_capacity': capacity
    }

    if storage_path in storj_node_pairs.keys():
        report_json['storj_node_id'] = storj_node_pairs[storage_path]

    print('Sending report for node ' + node_name)
    print(report_json)
    requests.post('https://www.storjdash.com/report', json=report_json)

def main():
    global SERVER_UUID
    global STORJSHARE_PATH
    try:
        settings_file = open('/etc/storjdash.json', 'r')
        settings_contents = settings_file.read()
        try:
            settings = json.loads(settings_contents)
            SERVER_UUID = settings['server_uuid']
            STORJSHARE_PATH = settings['storjshare_path']
            examine_configs(settings['configs_directory'])
        except KeyError:
            print('Invalid config file.  Exiting.')
        except json.JSONDecodeError:
            print('Corrupted config file.  Exiting.')
    except FileNotFoundError:
        print('Settings File Not Found.  Exiting.')
        exit(1)
