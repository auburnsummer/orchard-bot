from ob.message_builder import MessageBuilder
import httpx

from .constants import APPLICATION_ID, DISCORD_API_URL, BOT_TOKEN

base_url = f"{DISCORD_API_URL}/webhooks/{APPLICATION_ID}"

bot_auth = {'Authorization': f"Bot {BOT_TOKEN}"}

class Interactor:
    def __init__(self, token):
        self._token = token
        self.client = httpx.AsyncClient()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self.client.aclose()

    async def edit(self, mb: MessageBuilder, id):
        return await self.client.patch(
            f"{base_url}/{self._token}/messages/{id}",
            json=mb.payload(),
            headers=bot_auth
        )

    async def post(self, mb: MessageBuilder):
        return await self.client.post(
            f"{base_url}/{self._token}",
            json=mb.payload(),
            headers=bot_auth
        )