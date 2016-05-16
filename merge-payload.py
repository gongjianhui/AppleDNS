#!/usr/bin/env python3
import json
from argparse import ArgumentParser
from collections import OrderedDict, defaultdict
from urllib.parse import urlparse

from ipaddress import ip_address


def handle_ip(target):
    address = urlparse('http://%s' % target)
    return ip_address(address.hostname), address.port or 80


def merge_service(payloads):
    services = defaultdict(list)
    for service in sum(payloads, []):
        services[service['title']].append(service)
    for title, service in services.items():
        ips = defaultdict(list)
        domains = set()
        for x in service:
            domains |= set(x['domains'])
            for name, ipset in x['ips'].items():
                ipset = map(lambda item: item.strip(), ipset)
                ipset = list(set(ips[name]) | set(ipset))
                ips[name] = sorted(ipset, key=handle_ip)
        yield OrderedDict([
            ('title', title),
            ('domains', sorted(domains, key=lambda item: (len(item), item))),
            ('ips', OrderedDict(sorted(ips.items())))
        ])


def output(files):
    payloads = map(lambda filename: json.load(open(filename)), files)
    return json.dumps(
        sorted(merge_service(payloads), key=lambda item: item['title']),
        indent=4,
        ensure_ascii=False
    )


def main():
    parser = ArgumentParser()
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()

    print(output(args.files))

if __name__ == '__main__':
    main()
