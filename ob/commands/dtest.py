from ob.interactions import Interactor
from ob.message_builder import ActionRow, Button, MessageBuilder as M

async def dtest(body):
    async with Interactor(body["token"]) as i:
        await i.edit(M().content("ayayayayayaya"), "@original")

        await i.post(
            M()
            .content("popopopopo")
            .ephemeral()
            .row(
                ActionRow(
                    Button(label="HELLO")
                )
            )
        )

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
