# -*- coding: utf-8 -*-
"""
testifi.pypi
~~~~~~~~~~~~

This module contains the portions of testifi code that know how to handle
interacting with PyPI.
"""
import treq
import structlog

from twisted.internet.defer import inlineCallbacks, returnValue


logger = structlog.getLogger()


@inlineCallbacks
def certifiVersions():
    """
    This function determines what certifi versions are available and can be
    tested. It uses as its baseline the 14.05.14 release of certifi, and will
    locate all other verisons.

    :returns: A Deferred that fires with a list of tuples of certifi versions
        and tarball URLs.
    """
    log = logger.new(function='certifiVersions')
    r = yield treq.get('https://pypi.python.org/pypi/certifi/json', timeout=5)
    log.msg("got certifi versions!")
    data = yield r.json()

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
            continue

        log.msg("new release located", version=version, tarball=file[u'url'])
        result.append((version, file[u'url']))

    returnValue(result)


@inlineCallbacks
def downloadFile(remote_path, fobj):
    """
    Download a file over HTTP from ``remote_path`` and save it to the provided
    file object ``fobj``.
    """
    logger.msg(
        "downloading file", remote_path=remote_path, function='downloadFile'
    )

    def file_writer(data):
        fobj.write(data)

    remote_path = remote_path.encode('utf-8')
    r = yield treq.get(remote_path, timeout=5)
    try:
        yield treq.collect(r, file_writer)
    except Exception as e:
        print e
        raise
