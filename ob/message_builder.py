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