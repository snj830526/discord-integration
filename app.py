import discord
import os
import time

from datetime import datetime
from other_app import OtherApp

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger


TOKEN=os.environ['DISCORD_TOKEN']
CHANNEL_ID=os.environ['DISCORD_CHANNEL_ID']
other=OtherApp()


class DiscordClient(discord.Client):
    
    
    async def start_working(self):
        channel = self.get_channel(int(CHANNEL_ID))
        message = f'[현재시간] {self.get_date()} {self.get_time()}'
        await channel.send(message)
        
    
    async def on_ready(self):
        
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.start_working, CronTrigger(hour="*", minute="*", second="30"))
        scheduler.start()
        
        
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
                
            if 'refresh' in received.lower():
                codes = other.refreshMarketCodes()
                print(f'size : {len(codes)}')
                msg = f'[갱신] market codes : {len(codes)} 건'
                msg += ' {0.author.mention}'.format(message)
                print(msg)
                await message.channel.send(msg)
                
            if 'show' in received.lower():
                codes = other.getMarketCodes()
                print(f'size : {len(codes)}')
                msg = f'[조회] market codes : {len(codes)} 건'
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
            
           
    def get_time(self):
        return datetime.today().strftime('%H:%M:%S')
    
    
    def get_date(self):
        return datetime.today().strftime('%Y년 %m월 %d일')
            

intents = discord.Intents.default()
intents.message_content=True

client = DiscordClient(intents=intents)

client.run(TOKEN)
