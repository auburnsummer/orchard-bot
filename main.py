# Load and run dotenv before everything else
from dotenv import load_dotenv
import httpx
load_dotenv()

import json
from collections import defaultdict

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import uvicorn

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from ob.slash_router import SlashOption, SlashOptionPermission, SlashRoute, SlashRouter
from ob.constants import DB_PATH, DB_URL, PATHLAB_ROLE, OptionType, PUBLIC_KEY, PermissionType, ResponseType
from ob.register import get_command_to_id_mapping, update_slash_commands, update_slash_permissions
from pathlib import Path

import ob.commands as commands

import ob.crosscode as crosscode

# All the routes we're using go here.
router = SlashRouter(routes=[
    SlashRoute(name='ping', description='responds with pong!', handler=commands.ping),
    SlashRoute(
        name='zpasscode',
        description='return a passcode for pathlab use (pathlab people only)',
        options=[
            SlashOption(type=OptionType.STRING, name="check", description="put a passcode here to check it", required=False)
        ],
        handler=commands.passcode,
        defer=True
    )
])

"""
Starlette handler for the /interactions endpoint.
"""
async def interaction_handler(request):
    # Check the headers are correct: https://discord.com/developers/docs/interactions/slash-commands#security-and-authorization
    verify_key = VerifyKey(bytes.fromhex(PUBLIC_KEY))
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
        return JSONResponse({'type' : ResponseType.PONG})

    # handle slash commands...
    if body['type'] == 2:
        return router.handle(body)

    # handle components (button clicks, etc...)
    # under our model, all components are per-interaction (we don't have "permanent" buttons)
    if body['type'] == 3:
        return await crosscode.handle(body)
    
    print(body)
    return JSONResponse({'hello': 'world'})

"""
Before launching, update the slash commands defined by the router.
"""
async def prerun_update_slash_commands():
    print("updating slash commands...")
    payload = router.api()
    print(payload)
    resp = (await update_slash_commands(payload)).json()
    print(resp)

    mapping = get_command_to_id_mapping(resp)
    print("updating permissions...")
    payload2 = router.permission_api(mapping)
    print(payload2)
    print((await update_slash_permissions(payload2)).json())
    print("done!")

"""
Before launching, if we don't have our copy of the db download it from api.rhythm.cafe
"""
async def prerun_get_db():
    db_path = Path(DB_PATH)
    if not db_path.is_file():
        print(f"no db found at {DB_PATH}, downloading...")
        async with httpx.AsyncClient() as client:
            r = await client.get(DB_URL)
            with open(DB_PATH, "wb") as f:
                f.write(r.content)
            print("downloaded.")

# two identical routes. this is so i can change it in discord developer options to check
# we are handling ping and auth correctly.
app = Starlette(debug=True, routes=[
    Route('/interactions', interaction_handler, methods=['POST']),
    Route('/interactions2', interaction_handler, methods=['POST'])
], on_startup=[
    prerun_update_slash_commands,
    prerun_get_db
])

# Discord requires HTTPS. I'm using a cloudflare proxy, but it should also be possible to use a reverse
# proxy + lets encrypt instead.
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)