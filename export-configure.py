#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals

import json
import os.path
import sys
from argparse import ArgumentParser
from collections import namedtuple
from math import isnan
from operator import attrgetter

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


def find_fast_ip(ipset):
    Item = namedtuple('Item', ['ip', 'avg_rtt'])

    def handle_delta(items):
        def handle(item):
            ip, delta = item
            delta = list(item for item in delta if item != None)
            if len(delta):
                return Item(ip, sum(delta) / float(len(delta)))
            return Item(ip, float('NaN'))
        return list(map(handle, items.items()))

    def handle_sorted():
        data = sum(list(map(handle_delta, ipset.values())), [])
        return sorted(data, key=attrgetter('avg_rtt'))

    iptable = handle_sorted()

    if len(iptable):
        ip, avg_rtt = iptable[0]
        return ip, avg_rtt


def export(payload, target):
    if not payload:
        return
    for service in sorted(payload, key=lambda item: item['title']):
        ip, avg_rtt = find_fast_ip(service['ips'])
        if isnan(avg_rtt):
            continue
        print('# %s (Avg RTT: %.3fms)' % (service['title'], avg_rtt))
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
