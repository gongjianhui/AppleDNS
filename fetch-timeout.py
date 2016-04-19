#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import json
import os.path
import random
import sys
from argparse import ArgumentParser
from collections import defaultdict
from contextlib import closing
from datetime import datetime
from multiprocessing.dummy import Pool as ParallelPool
from socket import AF_INET, IPPROTO_TCP, SOCK_STREAM, TCP_NODELAY, socket
from time import time

from io import open

if sys.version_info[0] == 2:
    from urlparse import urlparse
    str = unicode
else:
    from urllib.parse import urlparse


def check_requirements():
    def check_python_version():
        if 0x2000000 <= sys.hexversion <= 0x2070000:
            print('your "python" lower than 2.7.0 upgrade.')
            return False
        if 0x3000000 <= sys.hexversion <= 0x3040000:
            print('your "python" lower than 3.4.0 upgrade.')
            return False
        return True

    return check_python_version()


def request_with_socket(host, port, timeout):
    with closing(socket(AF_INET, SOCK_STREAM)) as connection:
        connection.setsockopt(IPPROTO_TCP, TCP_NODELAY, 1)
        connection.settimeout(timeout)
        connection.connect((host, port))


def timeit(callback):
    begin_time = time()
    callback()
    end_time = time()
    return end_time - begin_time


def request(target):
    host, port, timeout = target

    try:
        rtt = timeit(lambda: request_with_socket(host, port, timeout))
        return host, rtt * 1000
    except:
        return host, None


def fetch(payload, timeout, concurrent, testing_times):
    if not payload:
        return

    def handle_ip(target):
        address = urlparse('http://%s' % str(target))
        return address.hostname, address.port or 80, timeout

    def handle_ipset(ips):
        ips *= testing_times
        random.shuffle(ips)
        return ips

    with closing(ParallelPool(concurrent)) as pool:
        for service_item in payload:
            print(str(service_item['title']))
            print(', '.join(service_item['domains']))

            iptable = service_item['ips']
            for name, ips in iptable.items():
                print('\t%s' % name)

                iptable[name] = defaultdict(list)
                request_payload = map(handle_ip, handle_ipset(ips))
                for ip, delta in pool.imap_unordered(request, request_payload):
                    iptable[name][ip].append(delta)
                    if delta:
                        print('\t\t%-15s\t%.3fms' % (ip, delta))
    save_result(payload)


def load_payload(path):
    if os.path.exists(path):
        with open(path, encoding='UTF-8') as fp:
            return json.loads(fp.read())
    else:
        print('"%s" file not found.' % path)
        sys.exit(1)


def save_result(payload):
    target_filename = 'apple-cdn-speed.report'
    with open(target_filename, 'w', encoding='UTF-8') as fp:
        report_data = json.dumps(
            payload,
            sort_keys=True,
            indent=4,
            ensure_ascii=False
        )
        fp.write(str(report_data))


def main():
    parser = ArgumentParser()
    parser.add_argument(
        'payload',
        type=str,
        help='payload'
    )

    parser.add_argument(
        '--timeout',
        type=int,
        help='timeout (default: %(default)s) (unit ms)',
        dest='timeout',
        default=400
    )

    parser.add_argument(
        '--concurrent',
        type=int,
        help='concurrent (default: %(default)s)',
        dest='concurrent',
        default=10
    )

    parser.add_argument(
        '--testing_times',
        type=int,
        help='testing times (default: %(default)s)',
        dest='testing_times',
        default=20
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    fetch(
        load_payload(args.payload),
        timeout=args.timeout / 1000.0,
        concurrent=args.concurrent,
        testing_times=args.testing_times
    )


if __name__ == '__main__' and check_requirements():
    main()
