import discord
import os
import time

from datetime import datetime
from other_app import OtherApp


TOKEN=os.environ['DISCORD_TOKEN']
CHANNEL_ID=os.environ['DISCORD_CHANNEL_ID']
other=OtherApp()


class DiscordClient(discord.Client):
    
    
    async def on_ready(self):
        await self.start_working()
        
        
    async def on_message(self, message):
        received = message.content
        
        try:
        
            if received.lower() == 'ping':
                await message.channel.send('pong {0.author.mention}'.format(message))
                
            if 'sell' in received.lower():
                msg = f'[매도] your order : {received.strip("sell")}'
                msg += ' {0.author.mention}'.format(message)
                print(msg)
                await message.channel.send(msg)
                
            if 'show' in received.lower():
                msg = f'[잔고] your account balance ...'
                msg += ' {0.author.mention}'.format(message)
                print(msg)
                await message.channel.send(msg)
                
            if 'buy' in received.lower():
                msg = f'[매수] your order : {received.strip("buy")}'
                msg += ' {0.author.mention}'.format(message)
                print(msg)
                await message.channel.send(msg)
        
        except Exception as e:
            print(f'error: {e}')


    async def start_working(self):
        channel = self.get_channel(int(CHANNEL_ID))
        while True:
           time.sleep(60)
           message = f'[현재시간] {self.get_date()} {self.get_time()}'
           await channel.send(message)
           
           
    def get_time(self):
        return datetime.today().strftime('%H:%M:%S')
    
    
    def get_date(self):
        return datetime.today().strftime('%Y년 %m월 %d일')
            

intents = discord.Intents.default()
intents.message_content=True

client = DiscordClient(intents=intents)

client.run(TOKEN)
