import requests

server_url = 'https://api.upbit.com/v1/candles/'


class UpbitCandle:

    def get(self, unit='days', count=1, market='KRW-BTC'):
        print('get candle')
        headers = {"accept": "application/json"}
        res = requests.get(server_url + unit + f'?count={count}&market={market}', headers=headers)
        return res.json()
