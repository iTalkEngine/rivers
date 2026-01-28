from rivers.core.http import Request, Response


class RiversApplication:
    """
    Point d'entrée WSGI principal du framework Rivers.
    Responsable de :
    - créer l'objet Request
    - gérer les erreurs globales
    - retourner une Response
    """

    def __init__(self):
        pass  # router, middleware viendront ici plus tard

    def build_request(self, environ):
        """
        Construit un objet Request à partir de l'environnement WSGI.
        """
        method = environ.get("REQUEST_METHOD", "GET")
        path = environ.get("PATH_INFO", "/")

        headers = {}
        for key, value in environ.items():
            if key.startswith("HTTP_"):
                headers[key[5:].replace("_", "-").title()] = value

        return Request(
            method=method,
            path=path,
            headers=headers,
        )

    def handle_request(self, request):
        """
        Traitement principal de la requête.
        (Router viendra ici plus tard)
        """
        return Response(
            {
                "framework": "rivers",
                "status": "running",
                "path": request.path,
            }
        )

    def __call__(self, environ, start_response):
        """
        Interface WSGI.
        """
        try:
            request = self.build_request(environ)
            response = self.handle_request(request)
        except Exception as e:
            response = Response(
                {
                    "error": "Internal Server Error",
                    "detail": str(e),
                },
                status=500,
            )

        return response(environ, start_response)


# Instance WSGI exposée
app = RiversApplication()
