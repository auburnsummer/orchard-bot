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

    def api(self):
        return [r.api() for r in self._routes]

    def handle(self, body):
        return JSONResponse({
            "type" : 4,
            "data" : {
                "content": "pong!"
            }
        })
