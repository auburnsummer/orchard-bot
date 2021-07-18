import os

BOT_TOKEN = os.environ["BOT_TOKEN"]
PRIVATE_KEY = os.environ["PRIVATE_KEY"]
DISCORD_API_URL = "https://discord.com/api/v8"

# If specified, register guild-specific commands instead of global.
# this is because guild commands refresh instantly whereas global takes ~1 hr
DEV_GUILD = os.environ["DEV_GUILD"] if "DEV_GUILD" in os.environ else False
APPLICATION_ID = os.environ["APPLICATION_ID"]

class OptionType:
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9