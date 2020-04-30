import json
from functools import wraps

from flask import jsonify, request

jsonp_notice = """
// MediaCrush supports Cross Origin Resource Sharing requests.
// There is no reason to use JSONP; please use CORS instead.
// For more information, see https://mediacru.sh/docs/api"""


def json_output(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        def jsonify_wrap(obj):
            callback = request.args.get("callback", False)
            jsonification = jsonify(obj)
            if callback:
                jsonification.data = "%s(%s);\n%s" % (
                    callback,
                    jsonification.data,
                    jsonp_notice,
                )  # Alter the response
                jsonification.mimetype = "text/javascript"

            return jsonification

        result = f(*args, **kwargs)
        if isinstance(result, tuple):
            return jsonify_wrap(result[0]), result[1]
        if isinstance(result, dict):
            return jsonify_wrap(result)

        # This is a fully fleshed out  response, return it immediately
        return result

    return wrapper
