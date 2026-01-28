class Response:
    """
    Représente une réponse HTTP.
    """

    def __init__(self, content="", status=200, headers=None):
        self.content = content
        self.status = status
        self.headers = headers or {}

    def set_header(self, name, value):
        self.headers[name] = value

    def __repr__(self):
        return f"<Response [{self.status}]>"
