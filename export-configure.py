#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import argparse
import json
from collections import defaultdict

from io import open

formats = {
    'hosts': '{ip:<15} {domain}',
    'surge': '{domain} = {ip}',
    'merlin': 'address=/{domain}/{ip}',
}


def check_requirements():
    import sys

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
    table = defaultdict(list)
    for item in sum(ips.values(), []):
        table[item['ip']].append(item['delta'])
    table = map(
        lambda item: (item[0], sum(item[1]) / len(item[1])),
        table.items()
    )
    if len(table):
        ip, rt = sorted(table, key=lambda item: item[1])[0]
        return ip
    return None


def export(payload, target):
    for service in sorted(payload, key=lambda item: item['title']):
        fast_ip = find_fast_ip(service['ips'])
        print('# %(title)s' % service)
        for domain in sorted(service['domains'], key=len):
            template = '%s'
            if not fast_ip:
                template = '# %s'
            print(template % formats[target].format(domain=domain, ip=fast_ip))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'target',
        help='output target',
        default='surge',
        choices=sorted(formats.keys(), key=len)
    )
    args = parser.parse_args()
    payload = json.load(open('result.json', encoding='UTF-8'))
    export(payload, args.target)


if __name__ == '__main__' and check_requirements():
    main()
