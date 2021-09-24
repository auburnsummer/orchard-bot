from ob.utils import get_slash_args
from ob.interactions import Interactor

import ob.keys as keys
from ob.message_builder import MessageBuilder as M

async def passcode(body):
    [check] = get_slash_args(["check"], body)

    async with Interactor(body["token"]) as i:
        if check is not None:
            # branch where we're checking a passcode
            try:
                result = keys.check_passcode(check)
                await i.edit(M().content("✅"), "@original")
            except Exception as e:
                await i.edit(M().content(f"❌: {e}"), "@original")
        else:
            # branch where we're generating a passcode
            passcode = keys.gen_passcode()

            await i.edit(M().content("🙈"), "@original")

            await i.post(M().content(passcode).ephemeral())