#!/usr/bin/env python3
import argparse
import json
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
    return sorted(table, key=lambda item: item[1])[0][0]


def export(payload, target):
    for service in payload:
        fast_ip = find_fast_ip(service['ips'])
        if not fast_ip:
            break
        for domain in sorted(service['domains']):
            print(formats[target].format(domain=domain, ip=fast_ip))


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
    payload = json.load(open('result.json'))
    export(payload, args.target)


if __name__ == '__main__':
    main()
