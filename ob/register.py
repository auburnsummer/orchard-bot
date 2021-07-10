import os
import httpx

from .constants import BOT_TOKEN, APPLICATION_ID, DISCORD_API_URL, DEV_GUILD

bot_auth = {'Authorization': f"Bot {BOT_TOKEN}"}

# DEV_GUILD is False if env variable not defined
if DEV_GUILD:
    base_url = f"{DISCORD_API_URL}/applications/{APPLICATION_ID}/guilds/{DEV_GUILD}/commands"
else:
    base_url = f"{DISCORD_API_URL}/applications/{APPLICATION_ID}/commands"

"""
Get a list of all current slash commands.
"""
async def current_slash_commands():
    async with httpx.AsyncClient() as client:
        r = await client.get(base_url, headers=bot_auth)
    return r.json()

"""
Remove a global slash command.
"""
async def remove_slash_command(id):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{base_url}/{id}", headers=bot_auth)
    return r

"""
update slash commands
"""
async def update_slash_commands(commands):
    async with httpx.AsyncClient() as client:
        r = await client.put(f"{base_url}/commands", json=commands, headers=bot_auth)
    return r


