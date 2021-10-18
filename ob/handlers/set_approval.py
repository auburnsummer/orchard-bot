from starlette.applications import Starlette
from starlette.responses import JSONResponse

from ob.db import get_status, set_status
from ob import keys

async def set_approval(request):
    # authorization...
    try:
        if 'authorization' not in request.headers:
            raise ValueError("There should be an Authorization header, but there aint")
        token_type, token = request.headers['authorization'].split(" ")
        if (token_type.lower() != "bearer"):
            raise ValueError("Token type should be Bearer.")
        keys.check_passcode(token)

    except Exception as e:
        return JSONResponse({'error': str(e)}, 401)

    # return JSONResponse({'hello': 'world'}, 200);

    # get stuff out from the body?
    try:
        body = await request.json()
        await set_status(body['id'], body['value'])
        return JSONResponse(await get_status(body['id']))
    except Exception as e:
        return JSONResponse({'error': str(e)}, 500)
    
    
    
