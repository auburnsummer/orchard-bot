# Load and run dotenv before everything else
from dotenv import load_dotenv
load_dotenv()

import json
from collections import defaultdict

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from ob.slash_router import SlashOption, SlashRoute, SlashRouter
from ob.constants import OptionType, PRIVATE_KEY
from ob.register import update_slash_commands

import ob.commands as commands

# All the routes we're using go here.
router = SlashRouter(routes=[
    SlashRoute(name='ping', description='responds with pong!', handler=commands.ping),
    SlashRoute(
        name='add',
        description='add two numbers together',
        handler=commands.add, 
        options=[
            SlashOption(type=OptionType.INTEGER, name='a', description='the first number', required=True),
            SlashOption(type=OptionType.INTEGER, name='b', description='the second number', required=True)
        ]
    ),
    SlashRoute(
        name='dtest',
        description='testing deferred responses',
        handler=commands.dtest,
        defer=True
    )
])

"""
Starlette handler for the /interactions endpoint.
"""
async def interaction_handler(request):
    # Check the headers are correct: https://discord.com/developers/docs/interactions/slash-commands#security-and-authorization
    verify_key = VerifyKey(bytes.fromhex(PRIVATE_KEY))
    rheaders = defaultdict(str, request.headers)
    signature = rheaders["x-signature-ed25519"]
    timestamp = rheaders["x-signature-timestamp"]
    payload = await request.body()

    try:
        verify_key.verify(timestamp.encode() + payload, bytes.fromhex(signature))
    except BadSignatureError:
        return JSONResponse({'error': 'Invalid request signature'}, status_code=401)

    # If we've gotten here, headers are valid. now respond...
    body = await request.json()

    # handle ping event...
    if body['type'] == 1:
        return JSONResponse({'type' : 1})
    
    # otherwise, it goes to the router for further processing.
    return router.handle(body)

"""
Before launching, update the slash commands defined by the router.
"""
async def prerun_update_slash_commands():
    print("updating slash commands...")
    payload = router.api()
    print(json.dumps(payload))
    print(await update_slash_commands(payload))
    print("done!")

# two identical routes. this is so i can change it in discord developer options to check
# we are handling ping and auth correctly.
app = Starlette(debug=True, routes=[
    Route('/interactions', interaction_handler, methods=['POST']),
    Route('/interactions2', interaction_handler, methods=['POST'])
], on_startup=[
    prerun_update_slash_commands
])

# Discord requires HTTPS. I'm using a cloudflare proxy, but it should also be possible to use a reverse
# proxy + lets encrypt instead.
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)