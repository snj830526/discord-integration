import os
import requests
import json

code_file = 'market_codes.json'
api_url = 'https://api.upbit.com'


class OtherApp():

    def __init__(self):
        pass

    def get_market_codes(self, code=None):
        saved = self.read_codes()
        if saved is None or len(saved) == 0:
            url = f"{api_url}/v1/market/all?isDetails=true"
            headers = {"accept": "application/json"}
            res = requests.get(url, headers=headers)
            saved = self.save_codes(res.json())

        result = []
        if code is not None and code != '':
            for s in saved:
                if code.upper() in s["market"]:
                    print(f'found : {s["market_event"]}')
                    result.append(f'{s["market"]} / {s["korean_name"]}')
        else:
            result = saved

        return result

    def refresh_market_codes(self):
        if os.path.isfile(code_file):
            os.remove(code_file)

        return self.get_market_codes()

    def save_codes(self, codes):
        print('writing codes')
        with open(code_file, 'w') as json_file:
            json.dump(codes, json_file)

        return codes

    def read_codes(self):
        if os.path.isfile(code_file):
            with open(code_file, 'r') as json_file:
                if json_file is not None:
                    codes = json.load(json_file)
                    return codes
                else:
                    return dict()
        else:
            return dict()
