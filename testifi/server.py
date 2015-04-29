# -*- coding: utf-8 -*-
"""
testifi.server
~~~~~~~~~~~~~~

The primary server module in testifi.
"""
from twisted.web import server, resource
from twisted.internet import reactor


class TestCollectionResource(resource.Resource):
    """
    This resource manages the collection of tests. It accepts POST and GET
    requests.
    """
    # TODO: Actual logic.
    def render_GET(self, request):
        request.setHeader('Content-Type', 'application/json')
        return "{}"

    def render_POST(self, request):
        request.setHeader('Content-Type', 'application/json')
        return "{}"


def runServer():
    root = resource.Resource()
    root.putChild('tests', TestCollectionResource())

    site = server.Site(root)
    reactor.listenTCP(8080, site)
    reactor.run()


if __name__ == '__main__':
    runServer()
