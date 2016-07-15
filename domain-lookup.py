#!/usr/bin/python
# -*- coding: utf-8 -*-

import dns.resolver
from argparse import ArgumentParser
import json
import sys
import os.path
from argparse import ArgumentParser
from io import open

def load_from_json_file(path):
    if os.path.exists(path):
        with open(path, encoding='UTF-8') as dns_file:
            return json.loads(dns_file.read())
    else:
        print('"%s" file not found.' % path)
        sys.exit(1)

def dns_lookup(dns_servers, domains):
    def get_a_record(answers):
        for i in answers.response.answer:
            for j in i.items:
                try:
                    yield j.address
                except:
                    continue

    ips = set()
    for server in dns_servers:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [server]
        for domain in domains:
            answers = resolver.query(domain, 'A')
            for ip in get_a_record(answers):
                ips.add(ip)
    return sorted([ip for ip in ips])

def main():
    parser = ArgumentParser()
    parser.add_argument(
        '-d',
        type = str,
        dest = 'domain',
        help = 'domain list'
    )
    parser.add_argument(
        '-s',
        type = str,
        dest = 'server',
        help = 'dns list'
    )

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    dns_servers = load_from_json_file(args.server)
    groups = load_from_json_file(args.domain)
    for group in groups:
        group['ips'] = {args.server: dns_lookup(dns_servers, group['domains'])}
    print json.dumps(groups, sort_keys=True, indent=4)

if __name__ == '__main__':
    main()
