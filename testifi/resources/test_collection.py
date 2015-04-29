# -*- coding: utf-8 -*-
"""
testifi.resources.test_collection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A resource to manage the test collection endpoint in testifi.
"""
import json
import uuid

from twisted.web import resource


# For now, rather than having a proper database backend, we'll just have an
# in-memory 'data store'.
tests = []


class TestCollectionResource(resource.Resource):
    """
    This resource manages the collection of tests. It accepts POST and GET
    requests.
    """
    # TODO: Actual logic.
    def render_GET(self, request):
        request.setHeader('Content-Type', 'application/json')
        return json.dumps(tests)

    def render_POST(self, request):
        # Grab the request body and decode it as JSON.
        body = request.content.read()

        try:
            body = json.loads(body)
        except ValueError:
            return self.handleClientError(request)

        # There should be a single key here.
        try:
            domain = body['domain']
        except KeyError:
            return self.handleClientError(request)

        # Generate a test ID.
        test_id = str(uuid.uuid4())

        # TODO: Actually test something!
        tests.append({
            "test_id": test_id,
            "domain": domain,
            "results": {
                "2015.04.28": {"result": "success", "status": "complete"}
            }
        })

        request.setHeader('Content-Type', 'application/json')
        response_data = {
            "request_id": test_id,
            "test_versions": ["2015.04.28"]
        }
        return json.dumps(response_data)

    def handleClientError(self, request):
        """
        Returns a response that encodes information about a client error.
        """
        # TODO: Give a reason!
        request.setHeader('Content-Type', 'application/json')
        request.setResponseCode(400)
        return '{"error": "invalid body"}'
