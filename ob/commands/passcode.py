from ob.interactions import Interactor

import ob.keys as keys
from ob.message_builder import MessageBuilder as M

async def passcode(body):
    async with Interactor(body["token"]) as i:

        passcode = keys.gen_passcode()

        await i.edit(M().content("🙈"), "@original")

        await i.post(M().content(passcode).ephemeral())