import traceback
from rivers.core.http import Request, Response
from rivers.core.router import Router


class RiversApplication:
    def __init__(self, settings_module=settings):
        self.settings = settings_module
    """
    Application centrale WSGI de Rivers.
    Gère :
    - Request / Response
    - Router
    - Middleware (auth, log, sécurité)
    """

    def __init__(self, settings=None):
        self.settings = settings or {}
        self.router = Router()
        self.middlewares = []

        self.load_middlewares()
        self.load_routes()

    # ==================================================
    # INITIALISATION
    # ==================================================

    def load_middlewares(self):
        """
        Ordre IMPORTANT :
        sécurité → logs → auth
        """
        self.middlewares = [
            self.security_middleware,
            self.logging_middleware,
            self.auth_middleware,
        ]

    def load_routes(self):
        """
        Routes de base
        """

        def home(request):
            return Response({
                "framework": "rivers",
                "status": "running"
            })

        self.router.add("GET", "/", home)

    # ==================================================
    # REQUEST
    # ==================================================

    def build_request(self, environ):
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

    # ==================================================
    # MIDDLEWARES
    # ==================================================

    def security_middleware(self, request):
        """
        Sécurité de base :
        - méthodes autorisées
        - headers dangereux
        """
        allowed_methods = {"GET", "POST", "PUT", "DELETE"}
        if request.method not in allowed_methods:
            return Response(
                {"error": "Method Not Allowed"},
                status=405
            )

        return None

    def logging_middleware(self, request):
        """
        Logging simple (extensible plus tard)
        """
        print(f"[RIVERS] {request.method} {request.path}")
        return None

    def auth_middleware(self, request):
        """
        Auth de base :
        - prépare le terrain (pas de logique lourde ici)
        """
        request.user = None  # plus tard : session / token
        return None

    # ==================================================
    # CORE HANDLER
    # ==================================================

    def handle_request(self, request):
        # ➜ Middleware AVANT view
        for middleware in self.middlewares:
            response = middleware(request)
            if response:
                return response

        # ➜ Router
        view = self.router.resolve(request)
        if not view:
            return Response({"error": "Not Found"}, status=404)

        response = view(request)

        # ➜ Sécurité response (headers globaux)
        response.add_header("X-Frame-Options", "DENY")
        response.add_header("X-Content-Type-Options", "nosniff")

        return response

    # ==================================================
    # WSGI ENTRY
    # ==================================================

    def __call__(self, environ, start_response):
        try:
            request = self.build_request(environ)
            response = self.handle_request(request)

        except Exception as e:
            if self.settings.get("DEBUG"):
                response = Response(
                    {
                        "error": "Internal Server Error",
                        "trace": traceback.format_exc()
                    },
                    status=500
                )
            else:
                response = Response(
                    {"error": "Internal Server Error"},
                    status=500
                )

        return response(environ, start_response)


# Instance WSGI
app = RiversApplication()
