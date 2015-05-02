# -*- coding: utf-8 -*-
"""
testifi.pypi
~~~~~~~~~~~~

This module contains the portions of testifi code that know how to handle
interacting with PyPI.
"""
import treq

from twisted.internet.defer import inlineCallbacks, returnValue


@inlineCallbacks
def certifiVersions():
    """
    This function determines what certifi versions are available and can be
    tested. It uses as its baseline the 14.05.14 release of certifi, and will
    locate all other verisons.

    :returns: A Deferred that fires with a list of tuples of certifi versions
        and tarball URLs.
    """
    print "it begins!"
    r = yield treq.get('https://pypi.python.org/pypi/certifi/json', timeout=5)
    print "response!"
    data = yield r.json()
    print "data!"

    # Note: this takes advantage of the fact that certifi's releases have the
    # same version number sort order as lexicographical. If that changes,
    # this will break.
    releases = sorted(data[u'releases'].keys())

    first_release = releases.index('14.05.14')
    target_versions = releases[first_release:]

    result = []
    for version in target_versions:
        files = data[u'releases'][version]

        # Find the .tar.gz release.
        for file in files:
            if file[u'filename'].endswith(u'.tar.gz'):
                break
        else:
            raise RuntimeError("Unable to locate tarball!")

        result.append((version, file[u'url']))

    print result

    returnValue(result)
