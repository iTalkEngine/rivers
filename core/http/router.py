import re

class Route:
    def __init__(self, method, path, view):
        self.method = method.upper()
        self.path = path
        self.view = view
        self.param_names = []

        # compile regex pour paramètres type <id>, <slug>
        pattern = re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", path)
        self.regex = re.compile(f"^{pattern}$")

        self.param_names = re.findall(r"<(\w+)>", path)


class Router:
    """
    Router central de Rivers avec support URL parameters.
    """

    def __init__(self):
        self.routes = []

    def add(self, method, path, view):
        self.routes.append(Route(method, path, view))

    def resolve(self, request):
        for route in self.routes:
            if route.method != request.method:
                continue
            match = route.regex.match(request.path)
            if match:
                # Injecte params dans la requête
                request.params = match.groupdict()
                return route.view
        return None
