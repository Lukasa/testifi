# -*- coding: utf-8 -*-
"""
testifi.server
~~~~~~~~~~~~~~

The primary server module in testifi.
"""
import sys

import structlog

from twisted.web import server, resource
from twisted.internet import reactor
from twisted.internet.defer import DeferredQueue
from twisted.internet.task import LoopingCall
from twisted.python.log import startLogging

from testifi.resources.test_collection import TestCollectionResource
from testifi.supervisor import Supervisor


def printer(x):
    print x


def runServer():
    structlog.configure(
        processors=[structlog.twisted.EventAdapter()],
        logger_factory=structlog.twisted.LoggerFactory(),
    )
    startLogging(sys.stdout)
    sup = Supervisor(DeferredQueue())
    root = resource.Resource()
    root.putChild('tests', TestCollectionResource(sup))

    release_poll = LoopingCall(sup.pollForNewReleases)
    release_poll.start(300)

    sup.testLoop()

    site = server.Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()


if __name__ == '__main__':
    runServer()
