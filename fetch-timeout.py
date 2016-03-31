#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import json
import multiprocessing
import os.path
import random
import socket
import sys
from argparse import ArgumentParser
from contextlib import closing
from datetime import datetime

from io import open

if sys.version_info[0] == 2:
    from urlparse import urlparse
    str = unicode
else:
    from urllib.parse import urlparse

timeout = 400  # unit ms
concurrent = 10
testing_times = 10


def check_requirements():
    def check_python_version():
        if sys.hexversion >= 0x2000000 and sys.hexversion <= 0x2070000:
            print('your "python" lower than 2.7.0 upgrade.')
            return False
        if sys.hexversion >= 0x3000000 and sys.hexversion <= 0x3040000:
            print('your "python" lower than 3.4.0 upgrade.')
            return False
        return True

    return check_python_version()


def request(target):
    host, port = target
    try:
        begin_time = datetime.now()

        conn = socket.socket()
        conn.settimeout(timeout / 1000.0)
        conn.connect((host, port))

        end_time = datetime.now()

        delta = end_time - begin_time

        rt = (delta.seconds * 1000) + (delta.microseconds / 1000.0)
        return host, rt
    except socket.error as err:
        return host, False


def fetch(payload):
    if not payload:
        return

    def handle_ip(target):
        address = urlparse('http://%s' % str(target))
        return address.hostname, address.port or 80

    with closing(multiprocessing.Pool(concurrent)) as pool:
        for service_item in payload:
            print(str(service_item['title']))
            print(', '.join(service_item['domains']))
            for name, ips in service_item['ips'].items():
                ips = ips * testing_times
                random.shuffle(ips)
                ips = pool.map(request, map(handle_ip, ips))
                ips = sorted(
                    ({'ip': ip, 'delta': delta} for ip, delta in ips if delta),
                    key=lambda item: item['delta']
                )
                service_item['ips'][name] = ips
                print('\t%s' % name)
                for item in ips:
                    print('\t\t%(ip)-15s\t%(delta)sms' % item)
    return payload


def load_payload(path):
    if os.path.exists(path):
        with open(path, encoding='UTF-8') as fp:
            return json.loads(fp.read())


def save_result(payload):
    target_filename = 'apple-cdn-speed.report'
    with open(target_filename, 'w', encoding='utf-8') as fp:
        report_data = json.dumps(
            payload,
            sort_keys=True,
            indent=4,
            ensure_ascii=False
        )
        fp.write(str(report_data))


def main():
    parser = ArgumentParser()
    parser.add_argument('payload', help='payload')
    args = parser.parse_args()

    save_result(fetch(load_payload(args.payload)))


if __name__ == '__main__' and check_requirements():
    main()
