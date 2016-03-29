#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
    from collections import defaultdict
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
    import json
    import os.path
    from io import open
    target_filename = 'apple-cdn-speed.report'
    if os.path.exists(target_filename):
        return json.load(open(target_filename, encoding='UTF-8'))
    print('please run "fetch-timeout.py" build "%s".' % target_filename)


def main():
    from argparse import ArgumentParser
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
