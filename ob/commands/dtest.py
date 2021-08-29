from ob.interactions import Interactor

async def dtest(body):
    async with Interactor(body["token"]) as i:
        await i.edit({"content": "ayayayayayayaa"}, "@original")
