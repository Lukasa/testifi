# Testifi

Testifi is a web service designed to test various certifi versions against
a number of TLS-enabled web properties. It's intended to ensure that certain
bundles do or do not validate certain certificates.

## API

The following endpoints are exposed:

### `GET /tests`

Receive a list of all websites for which recent test data is available.

### `POST /tests`

Schedule a website for testing. Takes a JSON body containing, at minimum, the
domain name of the website to test:

    {"domain": "mkcert.org"}

Returns a JSON body containing details about the request, and a request ID:

    {
        "request_id": "25723C5B-7694-405E-ADCB-C95D0EBC66D8",
        "test_versions": ["master", "2015.04.28"]
    }

### `GET /tests/<id>`

Poll for a single test result. This returns a JSON document containing the
complete set of information for a single test ID, including the results for all
versions.

    {
        "domain": "mkcert.org",
        "results": {
            "master": {"result": "success", "status": "complete"},
            "2015.04.28": {"result": null, "status": "running"}
        }
    }

### `GET /tests/<id>/stream`

Stream the test results as they come in. Returns chunked encoded JSON
documents, with each document terminated by a newline. If no result arrives for
20 seconds, writes a single chunk-encoded newline to the stream as a keepalive.

The stream is terminated when all responses have been received.
