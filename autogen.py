# usage: autogen.py [-h] [-f {surge,hosts}] input(List.md)
#e.g. $python autogen.py -f surge /Users/yourUsername/Downloads/AppleDNS/List.md

"""
Copyright 2016 Guan Hao
https://gist.github.com/raptium/5a9675667b05529857d4

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

 http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import subprocess
import re
import argparse

TIME_P = re.compile(r'time=([\d\.]+) ?ms')
DOMAIN_P = re.compile(r'(?:\w+\.)+apple\.com')
IP_P = re.compile(r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}')


def ping(host):
    cmds = ['ping', '-c', '1', host]
    try:
        output = subprocess.check_output(cmds)
        m = TIME_P.search(output)
        if m is None:
            return -1
        return float(m.group(1))
    except:
        return -1


def find_fastest(hosts, n=5):
    hosts = [(host, ping(host)) for host in hosts]
    hosts = filter(lambda x: x[1] != -1, hosts)
    hosts = sorted(hosts, key=lambda x: x[1])[:n]
    return [t[0] for t in hosts]


def output_all(hosts, domains, fmt='surge'):
    # output
    hosts = find_fastest(hosts)
    for domain in domains:
        if fmt == 'surge':
            print '%s = %s' % (domain, hosts[0])
        elif fmt == 'hosts':
            print '%s\t%s' % (hosts[0], domain)
        elif fmt == 'merlin':
            print 'address=/%s/%s' % (domain, hosts[0])


def process_file(args):
    with open(args.input) as f:
        domains = set([])
        hosts = set([])
        for line in f:
            if line.startswith('##'):
                if len(hosts) > 0 and len(domains) > 0:
                    output_all(hosts, domains, args.format)
                    # reset
                    hosts = set([])
                    domains = set([])
                elif 'apple.com' in line:
                    for m in DOMAIN_P.finditer(line):
                        domains.add(m.group(0))
            else:
                for m in IP_P.finditer(line):
                    hosts.add(m.group(0))
        if len(hosts) > 0 and len(domains) > 0:
            output_all(hosts, domains, args.format)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='input file, eg. List.md')
    parser.add_argument('-f', dest='format', help='output format',
                        default='surge', choices=['surge', 'hosts', 'merlin'])
                        args = parser.parse_args()
                        process_file(args)