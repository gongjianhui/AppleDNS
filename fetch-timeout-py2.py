<<<<<<< Updated upstream
# Author:jannson,CC0
#!/usr/bin/env python
=======
<<<<<<< HEAD
<<<<<<< HEAD
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: jannson, CC0
=======
# Author:jannson,CC0
#!/usr/bin/env python
>>>>>>> origin/master
=======
# Author:jannson,CC0
#!/usr/bin/env python
>>>>>>> origin/master
>>>>>>> Stashed changes
import argparse
import json
from datetime import datetime
import itertools

timeout = 400  # unit ms
testing_times = 10


def check_requirements():
    import sys

    def check_python_version():
        if sys.hexversion <= 0x2070000:
            print('your "python" lower than 2.7.0 upgrade.')
            return False
        return True

    def check_is_use_proxy():
        from os import environ
        http_proxy = environ.get('http_proxy')
        HTTP_PROXY = environ.get('HTTP_PROXY')
        https_proxy = environ.get('https_proxy')
        HTTPS_PROXY = environ.get('HTTPS_PROXY')

        def output(name, value):
            if value:
                print('%s=%s' % (name, value))

        if http_proxy or HTTP_PROXY or https_proxy or HTTPS_PROXY:
            print('you are using a proxy test')
            output('http_proxy', http_proxy)
            output('HTTP_PROXY', HTTP_PROXY)
            output('https_proxy', https_proxy)
            output('HTTPS_PROXY', HTTPS_PROXY)
            print()

        return True

    return all(
        (
            check_python_version(),
            check_is_use_proxy()
        )
    )


def request(target):
    host, port = target
    from socket import socket
    from socket import error
    try:
        begin_time = datetime.now()

        conn = socket()
        conn.settimeout(timeout / 1000.0)
        conn.connect((host, port))

        end_time = datetime.now()

        delta = end_time - begin_time

        rt = (delta.seconds * 1000.0) + (delta.microseconds / 1000.0)
        return host, rt
    except error as err:
        return host, False


def handle_ip(target):
    from six.moves.urllib.parse import urlparse
    address = urlparse('http://%s' % target)
    return address.hostname, address.port or 80


def fetch(payload):
    for service_item in payload:
        print(service_item['title'])
        print(', '.join(service_item['domains']))
        for name, ips in service_item['ips'].items():
            ips = itertools.imap(request, map(handle_ip, ips * testing_times))
            ips = sorted(
                ({'ip': ip, 'delta': delta} for ip, delta in ips if delta),
                key=lambda item: item['delta']
            )
            service_item['ips'][name] = ips
            print('\t%s' % name)
            for item in ips:
                print('\t\t%(ip)-15s\t%(delta)sms' % item)
    return payload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--payload', dest='payload', default='payload.json')
    args = parser.parse_args()
    payload = fetch(json.load(open(args.payload)))
    json.dump(payload, open('result.json', 'w'))


if __name__ == '__main__' and check_requirements():
    main()
