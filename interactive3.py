#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Author: jannson, CC0
# Modified by Bit Ye
import json
import multiprocessing
from datetime import datetime
from collections import defaultdict

timeout = 400  # unit ms
concurrent = 10
testing_times = 10

formats = {
    'hosts': '{ip:<15} {domain}',
    'surge': '{domain} = {ip}',
    'merlin': 'address=/{domain}/{ip}',
}


def check_requirements():
    import sys

    def check_python_version():
        if sys.hexversion <= 0x3040000:
            print('your "python" lower than 3.4.0 upgrade.')
            return False
        return True

    def check_is_use_proxy():
        from os import environ
        http_proxy = environ.get('http_proxy')
        HTTP_PROXY = environ.get('HTTP_PROXY')
        https_proxy = environ.get('https_proxy')
        HTTPS_PROXY = environ.get('HTTPS_PROXY')

        def output(name, value):
            if value:
                print('%s=%s' % (name, value))

        if http_proxy or HTTP_PROXY or https_proxy or HTTPS_PROXY:
            print('you are using a proxy test')
            output('http_proxy', http_proxy)
            output('HTTP_PROXY', HTTP_PROXY)
            output('https_proxy', https_proxy)
            output('HTTPS_PROXY', HTTPS_PROXY)
            print()

        return True

    return all(
        (
            check_python_version(),
            check_is_use_proxy()
        )
    )


def request(target):
    host, port = target
    from socket import socket
    from socket import error
    try:
        begin_time = datetime.now()

        conn = socket()
        conn.settimeout(timeout / 1000.0)
        conn.connect((host, port))

        end_time = datetime.now()

        delta = end_time - begin_time

        rt = (delta.seconds * 1000.0) + (delta.microseconds / 1000.0)
        return host, rt
    except error as err:
        return host, False


def handle_ip(target):
    from urllib.parse import urlparse
    address = urlparse('http://%s' % target)
    return address.hostname, address.port or 80


def fetch(payload):
    with multiprocessing.Pool(concurrent) as pool:
        for service_item in payload:
            print(service_item['title'])
            print(', '.join(service_item['domains']))
            for name, ips in service_item['ips'].items():
                ips = pool.map(request, map(handle_ip, ips * testing_times))
                ips = sorted(
                    ({'ip': ip, 'delta': delta} for ip, delta in ips if delta),
                    key=lambda item: item['delta']
                )
                service_item['ips'][name] = ips
                print('\t%s' % name)
                for item in ips:
                    print('\t\t%(ip)-15s\t%(delta)sms' % item)
    return payload


def find_fast_ip(ips):
    table = defaultdict(list)
    for item in sum(ips.values(), []):
        table[item['ip']].append(item['delta'])
    table = map(
        lambda item: (item[0], sum(item[1]) / len(item[1])),
        table.items()
    )
    ip, rt = sorted(table, key=lambda item: item[1])[0]
    return ip


def export(payload, target):
    for service in sorted(payload, key=lambda item: item['title']):
        fast_ip = find_fast_ip(service['ips'])
        print('# %(title)s' % service)
        for domain in sorted(service['domains'], key=len):
            template = '%s'
            if not fast_ip:
                template = '# %s'
            print(template % formats[target].format(domain=domain, ip=fast_ip))


def make_choice_isp():
    print("Choose your ISP")
    print("Input 1, 2 or 3.")
    print("1 for ChinaUnicom/联通; 2 for ChinaNet/电信; 3 for CMCC/移动.")
    c = int(input("input:"))
    if c == 1:
        ISP = open("./ChinaUnicom.json", encoding='UTF-8')
    elif c == 2:
        ISP = open("./ChinaNet.json", encoding='UTF-8')
    elif c == 3:
        ISP = open("./CMCC.json", encoding='UTF-8')
    else:
        print("What does you input???")
    return ISP

def make_choice_config():
    print("Choose the Config Syntax")
    print("Input 1, 2 or 3.")
    print("1 for surge; 2 for hosts; 3 for merlin.")
    c = int(input("input:"))
    if c == 1:
        config = "surge"
    elif c == 2:
        config = "hosts"
    elif c == 3:
        config = "merlin"
    else:
        print("What does you input???")
    return config


def main():
    isp = make_choice_isp()
    config = make_choice_config()
    payload = fetch(json.load(isp))
    export(payload, config)


if __name__ == '__main__' and check_requirements():
    main()
