# -*- coding: utf-8 -*-
"""
testifi.certifi
~~~~~~~~~~~~~~~

This code contains the certifi-specific testing logic.

The main function of this code is to import certifi from a specific location
and then attempt to validate a single TLS connection.

Unlike most of the rest of the code, this code is not based on Twisted.
This is to make it a bit easier to follow the logic, and because it's too
simple to justify.
"""
import argparse
import socket
import ssl
import sys


def handle_arguments():
    """
    Handle the command line arguments.

    :returns: The location of certifi in the filesystem.
    """
    parser = argparse.ArgumentParser(description='Certifi tester')
    parser.add_argument(
        'certifi_path',
        metavar='CERTIFI PATH',
        help='Path to certifi directory'
    )
    parser.add_argument(
        'host',
        metavar='HOST',
        help='The host to attempt to connect to.'
    )
    args = parser.parse_args()
    return (args.certifi_path, args.host)


def test(bundle_path, host):
    """
    Test that a cert bundle validates the certificate against a given host.
    """
    c = ssl.create_default_context(cafile=bundle_path)
    s = socket.socket()
    s = c.wrap_socket(s, server_hostname=host)

    # TODO: Don't limit ourselves to port 443
    try:
        s.connect((host, 443))
    except ssl.CertificateError as e:
        print e
        return 1
    except ssl.SSLError as e:
        print e

        if 'certificate verify failed' in e.message:
            return 1
        else:
            return 2

    return 0


def main():
    certifi_path, host = handle_arguments()
    sys.path.insert(1, certifi_path)
    import certifi
    sys.exit(test(certifi.where(), host))


if __name__ == '__main__':
    main()
