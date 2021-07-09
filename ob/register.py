import os
import httpx

from .constants import BOT_TOKEN, APPLICATION_ID, DISCORD_API_URL, DEV_GUILD

bot_auth = {'Authorization': f"Bot {BOT_TOKEN}"}

if DEV_GUILD:
    base_url = f"{DISCORD_API_URL}/applications/{APPLICATION_ID}/commands"
else:
    base_url = f"{DISCORD_API_URL}/applications/{APPLICATION_ID}/commands"

"""
Get a list of all current GLOBAL slash commands.
"""
async def current_global_slash_commands():
    async with httpx.AsyncClient() as client:
        r = await client.get(f"{DISCORD_API_URL}/applications/{APPLICATION_ID}/commands", headers=bot_auth)
    return r.json()

"""
Remove a global slash command.
"""
async def remove_slash_command(id):
    async with httpx.AsyncClient() as client:
        r = await client.delete(f"{DISCORD_API_URL}/applications/{APPLICATION_ID}/commands/{id}", headers=bot_auth)
    return r

"""
update slash commands
"""
async def update_slash_commands(commands):
    async with httpx.AsyncClient() as client:
        r = await client.put(f"{DISCORD_API_URL}/applications/{APPLICATION_ID}/commands", json=commands, headers=bot_auth)
    return r


"""
mass update the current GLOBAL slash commands (idempotent)
"""
async def set_global_slash_commands(commands):
    current_commands = await current_global_slash_commands()
    command_names = [c["name"] for c in commands]

    # anything that exists currently that's not in the ones we're adding...
    to_remove = [c["id"] for c in current_commands if c["name"] not in command_names]

    # loop through deleting all them:
    for id in to_remove:
        await remove_slash_command(id)

    # then add!
    await update_slash_commands(commands)

    # and we'll return the newly updated commands...
    return await current_global_slash_commands()