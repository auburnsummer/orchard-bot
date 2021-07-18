from ob.constants import ResponseType
from starlette.responses import JSONResponse

from ob.utils import get_slash_args


def add(body):
    a, b = get_slash_args(['a', 'b'], body)
    out = f"{a + b}"
    return JSONResponse({"type": ResponseType.CHANNEL_MESSAGE_WITH_SOURCE, "data": {"content": out}})