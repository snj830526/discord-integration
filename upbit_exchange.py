import jwt
import hashlib
import os
import requests
import uuid
from urllib.parse import urlencode, unquote

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = 'https://api.upbit.com/v1/accounts'


class UpbitExchangeApp:

    def get_account(self):
        print("get")
        payload = {
            'access_key': access_key,
            'nonce': str(uuid.uuid4()),
        }
        jwt_token = jwt.encode(payload, secret_key)
        authorization = 'Bearer {}'.format(jwt_token)
        headers = {
            'Authorization': authorization,
        }
        res = requests.get(server_url, params=None, headers=headers)
        print(res)
        return res.json()
