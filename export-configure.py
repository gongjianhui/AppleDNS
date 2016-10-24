#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import json
import os.path
import sys
from argparse import ArgumentParser
from collections import namedtuple
from datetime import datetime
from math import isnan
from operator import attrgetter

from io import open

formats = {
    'hosts': '{ip:<15} {domain}',
    'surge': '{domain} = {ip}',
    'merlin': 'address=/{domain}/{ip}',
    'ros': 'add name {domain} address={ip}',
    'unbound': '{domain} IN A {ip}'
}


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


def find_fast_ip(ipset):
    Item = namedtuple('Item', ['tag', 'ip', 'avg_rtt'])

    def handle_delta(items):
        tag, delta_map = items

        def handle(item):
            ip, delta = item
            delta = list(item for item in delta if item != None)
            if delta:
                return Item(tag, ip, sum(delta) / float(len(delta)))
            return Item(tag, ip, float('NaN'))

        return list(map(handle, delta_map.items()))

    def handle_sorted():
        data = sum(list(map(handle_delta, ipset.items())), [])
        return sorted(filter(lambda x: x.avg_rtt>0, data), key=attrgetter('avg_rtt'))

    iptable = handle_sorted()
    return iptable[0] if iptable else None


def export(payload, target):
    if not payload:
        return
    print('# Build Date: %s (UTC)' % datetime.utcnow().isoformat())
    for service in sorted(payload, key=lambda item: item['title']):
        tag, ip, avg_rtt = find_fast_ip(service['ips'])
        if isnan(avg_rtt):
            continue
        print('# %s [%s] (Avg RTT: %.3fms)' % (service['title'], tag, avg_rtt))
        for domain in sorted(service['domains'], key=len):
            template = '%s' if ip else '# %s'
            print(template % formats[target].format(domain=domain, ip=ip))


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
        choices=sorted(formats.keys(), key=len)
    )

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    export(load_payload(), args.target)


if __name__ == '__main__' and check_requirements():
    main()
