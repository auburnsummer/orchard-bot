from ob.constants import ButtonStyle
from . import ActionRow

class MessageBuilder:
    def __init__(self):
        self._dict = {
            "content": "",
            "flags": 0
        }

    def content(self, content):
        self._dict["content"] = content
        return self

    # https://discord.com/developers/docs/interactions/receiving-and-responding#create-followup-message
    def ephemeral(self, yes=True):
        self._dict["flags"] = 64 if yes else 0
        return self

    def payload(self):
        return self._dict

    def row(self, row: ActionRow):
        if "components" not in self._dict:
            self._dict["components"] = []
        self._dict["components"].append(row.payload())
        return self

class ActionRow:
    def __init__(self, *components):
        self._components = components

    def payload(self):
        return {
            "type": 1,
            "components": [c.payload() for c in self._components]
        }

class Button:
    def __init__(
        self,
        style = ButtonStyle.PRIMARY,
        label = None,
        emoji = None,
        url = None, 
        disabled = False):
        # create a dictionary consisting only of the values given that were not None
        args = locals().copy()
        self._dict = {k: v for k, v in args.items() if v is not None}
        self._dict['custom_id'] = 'hipehiofwheofie'

    def payload(self):
        return self._dict