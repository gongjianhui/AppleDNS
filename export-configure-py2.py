#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import io
from collections import defaultdict

formats = {
    'hosts': '{ip:<15} {domain}',
    'surge': '{domain} = {ip}',
    'merlin': 'address=/{domain}/{ip}',
}


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
        print(('# %(title)s' % service).encode('utf8', 'ignore'))
        for domain in sorted(service['domains'], key=len):
            template = '%s'
            if not fast_ip:
                template = '# %s'
            print(template % formats[target].format(domain=domain, ip=fast_ip))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--target',
        dest='target',
        help='output target',
        default='surge',
        choices=formats.keys()
    )
    args = parser.parse_args()
    payload = json.load(io.open('result.json', encoding='UTF-8'))
    export(payload, args.target)


if __name__ == '__main__':
    main()