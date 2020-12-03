from flask import Response
import json


def MakeResponse(status_code=200, data=None, headers=None):
    r = Response(status=status_code, mimetype="application/json")
    if data:
        r.set_data(json.dumps(data))
    if headers:
        for header in headers:
            r.headers[header] = headers[header]

    return r
