#!/usr/bin/env python3
import json
import multiprocessing
from datetime import datetime

payload = json.load(open('payload.json'))
timeout = 400  # unit ms
concurrent = 10


def check_requirements():
    import sys

    def check_python_version():
        if sys.hexversion <= 0x3040000:
            print('your "python" lower than 3.4.0 upgrade.')
            return False
        return True

    def check_requests():
        from importlib.util import find_spec
        from distutils.version import StrictVersion
        if find_spec('requests'):
            import requests
            if StrictVersion(requests.__version__) <= StrictVersion('2.9.0'):
                print('your "requests" lower than 2.9.0 upgrade.')
                return False
            return True
        else:
            print('please install "requests".($python3 -m pip install requests)')
            return False

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
            check_requests(),
            check_is_use_proxy()
        )
    )


def request(ip):
    import requests
    try:
        begin_time = datetime.now()
        requests.head(
            'http://%s/' %
            ip,
            timeout=timeout / 1000.0
        )
        end_time = datetime.now()
        delta = end_time - begin_time
        return ip, delta.microseconds / 1000.0
    except Exception as e:
        return ip, False


def main():
    with multiprocessing.Pool(concurrent) as pool:
        for service_item in payload:
            print(service_item['title'])
            print(', '.join(service_item['domains']))
            for name, ips in service_item['ips'].items():
                ips = pool.map(request, ips * 3)
                ips = sorted(
                    ({'ip': ip, 'delta': delta} for ip, delta in ips if delta),
                    key=lambda item: item['delta']
                )
                service_item['ips'][name] = ips
                print('  %s' % name)
                for item in ips:
                    print('      %(ip)-15s    %(delta)sms' % item)
    json.dump(payload, open('result.json', 'w'))


if __name__ == '__main__' and check_requirements():
    main()
