#!/usr/bin/env python3
import argparse
import json
from operator import attrgetter

formats = {
    'hosts': '{ip} {domain}',
    'surge': '{domain} = {ip}',
    'merlin': 'address=/{domain}/{ip}',
}


def find_fast_ip(ips):
    items = sorted(sum(ips.values(), []), key=lambda item: item['delta'])
    return items[0].get('ip')


def export(payload, target):
    for service in payload:
        fast_ip = find_fast_ip(service['ips'])
        if not fast_ip:
            break
        for domain in service['domains']:
            print(formats[target].format(domain=domain, ip=fast_ip))


def main(args):
    payload = json.load(open('result.json'))
    export(payload, args.target)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-t',
        '--target',
        dest='target', help='output target',
        default='surge',
        choices=['surge', 'hosts', 'merlin']
    )
    args = parser.parse_args()
    main(args)
