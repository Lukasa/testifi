# -*- coding: utf-8 -*-
"""
testifi.resources.test_collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A resource to manage the test collection endpoint in testifi.
"""
from twisted.web import resource

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

