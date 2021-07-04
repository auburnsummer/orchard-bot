from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from dotenv import load_dotenv
from collections import defaultdict
import uvicorn
import os

from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

load_dotenv()

async def interaction_handler(request):
    # Check the headers are correct: https://discord.com/developers/docs/interactions/slash-commands#security-and-authorization
    verify_key = VerifyKey(bytes.fromhex(os.environ['PRIVATE_KEY']))
    signature = request.headers["X-Signature-Ed25519"] if "X-Signature-Ed25519" in request.headers else ""
    timestamp = request.headers["X-Signature-Timestamp"] if "X-Signature-Timestamp" in request.headers else ""
    payload = await request.body()

    try:
        verify_key.verify(timestamp.encode() + payload, bytes.fromhex(signature))
    except BadSignatureError:
        return JSONResponse({'error': 'Invalid request signature'}, status_code=401)

    # now respond...
    body = await request.json()

    if body['type'] == 1:
        return JSONResponse({'type' : 1})
    return JSONResponse({'hello': 'world'})

app = Starlette(debug=True, routes=[
    Route('/interactions', interaction_handler, methods=['POST']),
])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=80)