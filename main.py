from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from dotenv import load_dotenv
import uvicorn

load_dotenv()

async def handler(request):
    payload = await request.json()
    if payload['type'] == 1:
        return JSONResponse({'type' : 1})
    return JSONResponse({'hello': 'world'})

app = Starlette(debug=True, routes=[
    Route('/', handler, methods=['POST']),
])

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=9100)