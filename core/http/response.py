import json


class Response:
    """
    Réponse HTTP compatible WSGI.
    Supporte automatiquement le JSON si body est dict ou list.
    """

    status_codes = {
        200: "OK",
        201: "Created",
        204: "No Content",
        400: "Bad Request",
        401: "Unauthorized",
        403: "Forbidden",
        404: "Not Found",
        500: "Internal Server Error",
    }

    def __init__(self, body=b"", status=200, headers=None):
        self.status = status
        self.headers = headers or []

        #  Auto JSON
        if isinstance(body, (dict, list)):
            body = json.dumps(body)
            self.add_header("Content-Type", "application/json")

        # str → bytes
        if isinstance(body, str):
            body = body.encode("utf-8")

        self.body = body

        # Header obligatoire WSGI
        self.add_header("Content-Length", str(len(self.body)))

    def add_header(self, name, value):
        self.headers.append((name, value))

    @property
    def status_line(self):
        reason = self.status_codes.get(self.status, "")
        return f"{self.status} {reason}"

    def __call__(self, environ, start_response):
        start_response(self.status_line, self.headers)
        return [self.body]

    def __repr__(self):
        return f"<Response {self.status}>"
