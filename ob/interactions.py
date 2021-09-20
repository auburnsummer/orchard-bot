from ob.message_builder import MessageBuilder
import httpx

from .constants import APPLICATION_ID, DISCORD_API_URL, BOT_TOKEN
from uuid import uuid4

import ob.crosscode as cc

base_url = f"{DISCORD_API_URL}/webhooks/{APPLICATION_ID}"

bot_auth = {'Authorization': f"Bot {BOT_TOKEN}"}

class Interactor:
    """
    A class that contains methods for handling a slash command interaction.
    """
    def __init__(self, token):
        self._token = token
        self.client = httpx.AsyncClient()
        # list of crosscode uuids which this interactor owns
        self.crosscode_uuids = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        # remove any remaining UUIDS.
        for uuid in self.crosscode_uuids:
            cc.clean(uuid)
        await self.client.aclose()

    async def edit(self, mb: MessageBuilder, id):
        """
        Wrapper around discord API edit message.

        https://discord.com/developers/docs/resources/webhook#edit-webhook-message
        """
        return await self.client.patch(
            f"{base_url}/{self._token}/messages/{id}",
            json=mb.payload(),
            headers=bot_auth
        )

    async def post(self, mb: MessageBuilder):
        """
        Wrapper around discord API post message.

        https://discord.com/developers/docs/interactions/receiving-and-responding#create-followup-message
        """
        return await self.client.post(
            f"{base_url}/{self._token}",
            json=mb.payload(),
            headers=bot_auth
        )

    async def uuid(self):
        """
        Return a new UUID and register a future to it.
        """
        new_uuid = await cc.future()
        self.crosscode_uuids.append(new_uuid)
        return new_uuid