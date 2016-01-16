#!/usr/bin/env python
#-*- coding:utf-8 -*-
# Created by Clark 2016.01.07
# Contact Email: linchengkuang@foxmail.com
# Name: xxx.py
# This script is used to create or change A record by using Dnspod Python API
# Version 1.0


import httplib, urllib
import json
import socket
import sys
import time
import platform
import os
import subprocess

time.sleep(20)
username = 'Your Email Here'
password = 'Your Password Here'
format = 'json'
domain = [u'Your Domain Here']
params = {'login_email':username,'login_password':password,'format':format}

def file_extension(path):
    return os.path.splitext(path)[0]

def get_script_name():
    if platform.system() == "Windows":
        argv0_list = file_extension(__file__).split("\\")
        script_name = argv0_list[len(argv0_list) - 1];
    else:
        argv0_list = sys.argv[0].split("/")
        script_name_split = argv0_list[len(argv0_list) - 1];
        script_name_split = script_name_split.split('.')
        script_name = script_name_split[0]
    return script_name

def get_domain_info(domain):
    domain_split = domain.split('.')
    domain_split_len = len(domain_split)
    maindomain = domain_split[domain_split_len - 2] + '.' + domain_split[domain_split_len - 1]
    domain = get_script_name() + '.' + maindomain
    return maindomain,domain

def request(action, params, method = 'POST'):
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/json"}
    conn = httplib.HTTPSConnection("dnsapi.cn")
    conn.request(method, '/' + action, urllib.urlencode(params), headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()
    if response.status == 200:
        return data
    else:
        return None

def get_my_domain_id():
    data = request('Domain.List',params)
    data = json.loads(data)
    domainlist = data.get('domains')
    domaninfo = {}
    print domainlist
    for d in domainlist:
        domaninfo[d.get('name')]  = d.get('id')
    return domaninfo
my_domain_id_list = get_my_domain_id()

def get_my_domain_record_id(domain_id):
    params['domain_id'] = domain_id
    data = request('Record.List',params)
    data = json.loads(data)
    if data.get('code') == '10':
        return None
    domainname = data.get('domain').get('name')
    record_list = data.get('records')
    record = {}
    for r in record_list:
        if r.get('type') == 'A':
            key = r.get('name') != '@' and r.get('name') + '.' + domainname or domainname
            record[key] = {'id':r.get('id'),'value':r.get('value')}
    return record

def addrecord(domain_id,ip):
    params['domain_id'] = domain_id
    params['record_type'] = 'A'
    params['record_line'] = '默认'
    params['sub_domain'] = get_script_name()
    params['value'] = ip
    params['ttl'] = 600
    request('Record.Create',params)

def changerecord(domain_id,record_id,ip):
    params['domain_id'] = domain_id
    params['record_id'] = record_id
    params['record_line'] = '默认'
    params['sub_domain'] = get_script_name()
    params['value'] = ip
    params['ttl'] = 600
    request('Record.Ddns',params)

def getip():
    sock = socket.create_connection(('ns1.dnspod.net', 6666))
    ip = sock.recv(16)
    sock.close()
    return ip or None

def networkcheck():
    check = open(os.devnull, 'w')
    return1 = subprocess.call('ping -c 1 baidu.com', shell = True, stdout = check, stderr = check)
    if return1:
        os.system('rasdial adsl')
    check.close()


def updatedomaininfo(domain):
    m,sub_m = get_domain_info(domain)
    domain_id = my_domain_id_list.get(m)
    record_list = get_my_domain_record_id(domain_id)
    if record_list == None:
        return None
    rocord_info = record_list.get(sub_m)
    if rocord_info == None:
        return sub_m,None,None,domain_id
    else:
        record_ip = rocord_info.get('value')
        record_id = rocord_info.get('id')
        return sub_m,record_ip,record_id,domain_id

if __name__ == '__main__':
    while True:
        try:
            print 1
            for dm in domain:
                domaindata = updatedomaininfo(dm)
                if domaindata == None:
                    continue
                dnsdomain,dnsdmainip,record_id,domain_id = domaindata
                domain_name = dnsdomain.split('.')[0]
                ip = getip()
                if record_id == None:
                    print "Process Add Record"
                    addrecord(domain_id,ip)
                else:
                    if ip == dnsdmainip:
                        continue
                    else:
                        print "Process Change Record"
                        changerecord(domain_id,record_id,ip)
        except Exception, e:
            print e
            pass
        time.sleep(30)
        networkcheck()
