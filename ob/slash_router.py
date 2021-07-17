# class Option:
#     def __init__(self, type, name, description, required=False, choices=None, options=None):
#         self._type = type
#         self._name = name
#         self._description = description
#         self._required = required
#         self._choices = choices
#         self._options = options

from starlette.responses import JSONResponse

class SlashRoute:
    def __init__(self, name, description, handler, default_permission=True):
        self._name = name
        self._description = description
        self._handler = handler
        self._default_permission = default_permission

    def api(self):
        return {
            'name' : self._name,
            'description': self._description,
            'default_permission': self._default_permission
        }

class SlashRouter:
    def __init__(self, routes):
        self._routes = routes
        # build a mapping of route names to routes
        self._route_map = {}
        for route in self._routes:
            self._route_map[route._name] = route

    def api(self):
        return [r.api() for r in self._routes]

    def handle(self, body):
        # Get the route name from the body. The body is a dictionary. The route name is located under the key "data.name"
        route_name = body['data']['name']
        # Check if the route name is present in the mapping.
        if route_name in self._route_map:
            # Execute the associated handler.
            return self._route_map[route_name]._handler(body)
        else:
            # Otherwise, return a default response. The default response has a 200 return code.
            # The key 'type' is 4, and the key 'data.content' is something like "oh no"
            return JSONResponse({"type": 4, "data": {"content": "oh no"}})


