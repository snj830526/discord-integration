import discord
import os


TOKEN=os.environ['DISCORD_TOKEN']
CHANNEL_ID=os.environ['DISCORD_CHANNEL_ID']


class MyClient(discord.Client):
    
    async def on_ready(self):
        channel = self.get_channel(int(CHANNEL_ID))
        await channel.send('hello~.')
        
        
    async def on_message(self, message):
        received = message.content
        
        if received.lower() == 'ping':
            print('pong')
            await message.channel.send('pong{0.author.mention}'.format(message))


intents = discord.Intents.default()
intents.message_content=True
client = MyClient(intents=intents)
client.run(TOKEN)
