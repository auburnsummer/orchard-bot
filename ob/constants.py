import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
PRIVATE_KEY = os.environ["PRIVATE_KEY"]
DISCORD_API_URL = "https://discord.com/api/v8"

# If specified, register guild-specific commands instead of global.
# this is because guild commands refresh instantly whereas global takes ~1 hr
DEV_GUILD = os.environ["DEV_GUILD"] if "DEV_GUILD" in os.environ else False
APPLICATION_ID = os.environ["APPLICATION_ID"]