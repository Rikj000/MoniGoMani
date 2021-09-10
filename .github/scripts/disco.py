import os

from discord import Client

# Initialize the dance floor
disco_bot = os.environ['DISCO_BOT']
disco_token = os.environ['DISCO_TOKEN']
disco_channel = os.environ['DISCO_CHANNEL']
disco_message = os.environ['DISCO_MESSAGE']


class Disco(Client):
    def __init__(self, *args, **kwargs):
        Client.__init__(self, **kwargs)

    # Ready to party!
    async def on_ready(self):
        channel = self.get_channel(int(disco_channel))
        await channel.send(disco_message)
        await self.close()


disco = Disco()
disco.run(disco_token, bot=bool(disco_bot))
