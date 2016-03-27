#!/usr/bin/env python3
import argparse
import json
from collections import defaultdict

from ipaddress import ip_address


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
                ipset = list(set(ips[name]) | set(ipset))
                ipset = map(lambda item: item.strip(), ipset)
                ips[name] = sorted(ipset, key=lambda item: ip_address(item))
        yield {
            'title': title,
            'ips': ips,
            'domains': list(domains)
        }


def output(files):
    payloads = map(lambda filename: json.load(open(filename)), files)
    print(
        json.dumps(
            list(merge_service(payloads)),
            sort_keys=True,
            indent=4,
            ensure_ascii=False
        )
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('files', nargs='+')
    args = parser.parse_args()
    output(args.files)

if __name__ == '__main__':
    main()
