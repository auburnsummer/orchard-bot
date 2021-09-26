from ob.interactions import Interactor
from ob.message_builder import MessageBuilder as M
from ob.utils import get_slash_args
from ob.statuses import get_status


async def approve(body):
    async with Interactor(body["token"]) as i:
        id, approval = get_slash_args(['id', 'approval'], body)
        if approval is None:
            # getting an approval route
            row = get_status(id)
            message = M() \
                .content(f"{row['id']}: {row['approval']}")
            await i.edit(message, "@original")
            pass
        else:
            print(id)
            print(approval)
            await i.edit(M().content("efefefef"), "@original")