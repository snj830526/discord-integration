import os
from datetime import datetime
import json

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from upbit_app import UpbitApp
from upbit_candle import UpbitCandle
from upbit_exchange import UpbitExchangeApp

TOKEN = os.environ['DISCORD_TOKEN']
CHANNEL_ID = os.environ['DISCORD_CHANNEL_ID']

upbitApp = UpbitApp()
upbitCandle = UpbitCandle()
upbitExchange = UpbitExchangeApp()


class DiscordClient(discord.Client):

    async def start_working(self):
        channel = self.get_channel(int(CHANNEL_ID))
        message = f'[현재시간] {self.get_date()} {self.get_time()}'
        await channel.send(message)

    async def on_ready(self):
        scheduler = AsyncIOScheduler()
        scheduler.add_job(self.start_working, CronTrigger(hour="*", minute="0", second="0"))
        scheduler.start()

    async def on_message(self, message):
        received = message.content

        try:
            if received.lower() == 'ping':
                await message.channel.send('pong {0.author.mention}'.format(message))

            if received.lower().startswith('sell'):
                msg = f'[매도] your order : {received.strip("sell")}'
                msg += ' {0.author.mention}'.format(message)
                print(msg)
                await message.channel.send(msg)

            if received.lower().startswith('refresh'):
                codes = upbitApp.refresh_market_codes()
                msg = f'[갱신] market codes : {len(codes)} 건'
                msg += ' {0.author.mention}'.format(message)
                print(msg)
                await message.channel.send(msg)

            if received.lower().startswith('show'):
                code = received.lower().strip("show").strip()
                codes = upbitApp.get_market_codes(code)
                msg = f'[조회] market codes : {len(codes)} 건'
                msg += ' {0.author.mention}'.format(message)
                print(msg)
                await message.channel.send(msg)

            if received.lower().startswith('account'):
                account = upbitExchange.get_account()
                msg = f'[잔고] {account}'
                msg += ' {0.author.mention}'.format(message)
                print(msg)
                await message.channel.send(msg)

            if received.lower().startswith('candle'):
                inputs = received.lower().split(' ')
                unit = self.get_candle_unit(inputs)
                count = self.get_candle_count(inputs)
                market = self.get_candle_market(inputs)
                outputs = upbitCandle.get(unit=unit, count=count, market=market)
                outputs.reverse()
                msg = f'[캔들] {self.json_string_pretty(outputs)}'
                msg += ' {0.author.mention}'.format(message)
                print(msg)
                await message.channel.send(msg)

            if received.lower().startswith('buy'):
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

    def get_candle_inputs(self, inputs, index):
        try:
            return inputs[index]
        except:
            return None

    def get_candle_unit(self, inputs):
        unit = 'days' if self.get_candle_inputs(inputs, 1) is None else self.get_candle_inputs(inputs, 1)
        if unit.startswith('minutes'):
            res = f'minutes/{unit.strip("minutes")}'
        elif unit in ['days', 'weeks', 'months']:
            res = unit
        else:
            raise Exception(f'candle unit error :: {unit}')
        return res

    def get_candle_count(self, inputs):
        return 1 if self.get_candle_inputs(inputs, 2) is None else self.get_candle_inputs(inputs, 2)

    def get_candle_market(self, inputs):
        return 'KRW-BTC' if self.get_candle_inputs(inputs, 3) is None else self.get_candle_inputs(inputs, 3).upper()

    def json_string_pretty(self, json_str):
        return json.dumps(json_str, indent=4)


intents = discord.Intents.default()
intents.message_content = True

client = DiscordClient(intents=intents)

client.run(TOKEN)
