#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import json
import os.path
import sys
from argparse import ArgumentParser

from io import open

formats = {
    'hosts': '{ip:<15} {domain}',
    'surge': '{domain} = {ip}',
    'merlin': 'address=/{domain}/{ip}',
}


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


def find_fast_ip(ips):
    def handle_delta(item):
        ip, delta = item
        return ip, sum(delta) / len(delta)

    def handle_ips(item):
        return list(map(handle_delta, item.items()))

    iptable = sorted(
        sum(list(map(handle_ips, ips.values())), []),
        key=lambda item: item[1]
    )

    if len(iptable):
        ip, rt = iptable[0]
        return ip


def export(payload, target):
    if not payload:
        return
    for service in sorted(payload, key=lambda item: item['title']):
        fast_ip = find_fast_ip(service['ips'])
        print('# %(title)s' % service)
        for domain in sorted(service['domains'], key=len):
            template = '%s'
            if not fast_ip:
                template = '# %s'
            print(template % formats[target].format(domain=domain, ip=fast_ip))


def load_payload():
    target_filename = 'apple-cdn-speed.report'
    if os.path.exists(target_filename):
        return json.load(open(target_filename, encoding='UTF-8'))
    print('please run "fetch-timeout.py" build "%s".' % target_filename)


def main():
    parser = ArgumentParser()
    parser.add_argument(
        'target',
        help='output target',
        default='surge',
        choices=sorted(formats.keys(), key=len)
    )
    args = parser.parse_args()

    export(load_payload(), args.target)


if __name__ == '__main__' and check_requirements():
    main()
