# Load and run dotenv before everything else
from dotenv import load_dotenv
load_dotenv()

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from collections import defaultdict
import uvicorn
import os

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

from ob.slash_router import SlashRoute, SlashRouter
from ob.constants import PRIVATE_KEY


router = SlashRouter(routes=[
    SlashRoute(name='ping', description='responds with pong!', handler=None)
])

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

    # now respond...
    body = await request.json()

    # handle ping event...
    if body['type'] == 1:
        return JSONResponse({'type' : 1})
    
    return router.handle(body)

# two identical routes. this is so i can change it in discord developer options to check
# we are handling ping and auth correctly.
app = Starlette(debug=True, routes=[
    Route('/interactions', interaction_handler, methods=['POST']),
    Route('/interactions2', interaction_handler, methods=['POST'])
])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)