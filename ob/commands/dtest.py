from ob.interactions import Interactor
from ob.message_builder import MessageBuilder

async def dtest(body):
    async with Interactor(body["token"]) as i:
        await i.edit(MessageBuilder().content("ayayayayayaya"), "@original")

        await i.post(MessageBuilder().content("popopopopo").ephemeral())

        # await i.post({
        #     "content": "popopopopopo",
        #     "components": [
        #         {
        #             "type": 1,
        #             "components": [
        #                 {
        #                     "type": 2,
        #                     "label": "Click me!",
        #                     "style": 1,
        #                     "custom_id": "click_one"
        #                 }
        #             ]
        #         }
        #     ]
        # })
