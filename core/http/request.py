class Request:
    """
    Représente une requête HTTP entrante.
    Inspirée de Django HttpRequest Simplifiée et maîtrisée.
    """

    def __init__(self, method, path, headers=None, query=None, body=None):
        self.method = method.upper()
        self.path = path

        self.headers = headers or {}
        self.query = query or {}
        self.body = body

    def get_header(self, name, default=None):
        """Récupère un header HTTP"""
        return self.headers.get(name, default)

    def __repr__(self):
        return f"<Request {self.method} {self.path}>"
