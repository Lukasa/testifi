# -*- coding: utf-8 -*-
"""
testifi.server
~~~~~~~~~~~~~~

The primary server module in testifi.
"""
from twisted.web import server, resource
from twisted.internet import reactor

from testifi.resources.test_collection import TestCollectionResource


def runServer():
    root = resource.Resource()
    root.putChild('tests', TestCollectionResource())

    site = server.Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()


if __name__ == '__main__':
    runServer()
