# -*- coding: utf-8 -*-
"""
testifi.supervisor
~~~~~~~~~~~~~~~~~~

This module contains code that manages the environment of testifi.
"""
import collections
import os.path
import tempfile

import distutils.spawn
import structlog

from twisted.internet.defer import (
    inlineCallbacks, DeferredSemaphore, returnValue
)
from twisted.internet.utils import getProcessValue, getProcessOutput

from testifi.pypi import certifiVersions, downloadFile


logger = structlog.getLogger()


Test = collections.namedtuple('Test', ['id', 'host'])


class Supervisor(object):
    """
    The Supervisor class manages the environments of testifi, and allows
    scheduling of work.
    """
    def __init__(self, queue):
        self.managedPackageVersions = set()
        self.certifiDirectory = tempfile.mkdtemp()
        self.testSemaphore = DeferredSemaphore(tokens=32)
        self.binPath = os.path.join(
            os.path.split(__file__)[0], 'certifi_test.py'
        )
        self.queue = queue
        self._log = logger.new(object="supervisor")

    @inlineCallbacks
    def pollForNewReleases(self):
        """
        Check whether any new certifi releases have been made.
        """
        log = self._log.bind(function="pollForNewReleases")
        log.msg("polling for new releases")

        releases = yield certifiVersions()

        for release, file in releases:
            if release in self.managedPackageVersions:
                log.msg("skipping existing release", release=release)
                continue

            # The release is new. We need to start processing it.
            yield self.addNewRelease(release, file)

    @inlineCallbacks
    def addNewRelease(self, release, tarball_path):
        """
        For each new release that we've discovered, set up processing for it.
        """
        log = self._log.bind(function="addNewRelease", release=release)
        log.msg("adding release")

        # Download the tarball.
        file_path = os.path.join(
            self.certifiDirectory, 'certifi-' + release + '.tar.gz'
        )
        with open(file_path, 'wb') as f:
            yield downloadFile(tarball_path, f)

        log.msg("tarball saved", tarball=file_path)

        rc = yield getProcessValue(
            distutils.spawn.find_executable('tar'),
            args=['xvf', file_path, '-C', self.certifiDirectory]
        )
        assert not rc

        log.msg("adding to managed versions")
        self.managedPackageVersions.add(release)

    @inlineCallbacks
    def _testHostAgainstRelease(self, host, release):
        """
        Tests a given host against a specific certifi release. Returns a
        Deferred that fires with the result of the test.
        """
        log = self._log.bind(function="_testHostAgainstRelease")
        file_path = os.path.join(self.certifiDirectory, 'certifi-' + release)
        args = [self.binPath, file_path, host]
        log.msg("running test", args=args)

        result = yield getProcessValue(
            distutils.spawn.find_executable('pypy'),
            args=args,
        )
        returnValue(result)

    @inlineCallbacks
    def testHost(self, host):
        """
        Runs the certifi tests against a given host.

        Returns a deferred that fires with a list of tuples: certifi release
        and whether the test passed.
        """
        log = self._log.bind(function="testHost", host=host)
        results = []
        for release in self.managedPackageVersions:
            result = yield self.testSemaphore.run(
                self._testHostAgainstRelease, host, release
            )
            results.append((release, result))
            log.msg("test complete", release=release, result=result)

        returnValue(results)

    @inlineCallbacks
    def testLoop(self):
        """
        Loop forever, popping tests off the queue and running them.
        """
        log = self._log.bind(function="testLoop")
        while True:
            test = yield self.queue.get()
            log = log.bind(test_id=test.id, host=test.host)
            log.msg("beginning test")
            try:
                results = yield self.testHost(test.host)
            except Exception as e:
                print e
                continue
            log.msg("test suite complete", results=results)
