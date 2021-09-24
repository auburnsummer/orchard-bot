from starlette.responses import FileResponse, JSONResponse
from ob.constants import DB_PATH

async def orchard_dot_db(request):
    return FileResponse(DB_PATH, media_type="application/x-sqlite3")