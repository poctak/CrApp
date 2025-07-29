import requests
import time
import hmac
import hashlib

API_KEY = 'TVŮJ_API_KEY'
SECRET_KEY = 'TVŮJ_SECRET_KEY'

base_url = 'https://api.binance.com'

def get_account_info():
    endpoint = '/api/v3/account'
    timestamp = int(time.time() * 1000)
    query_string = f'timestamp={timestamp}'
    signature = hmac.new(SECRET_KEY.encode(), query_string.encode(), hashlib.sha256).hexdigest()

    headers = {'X-MBX-APIKEY': API_KEY}
    url = f'{base_url}{endpoint}?{query_string}&signature={signature}'

    response = requests.get(url, headers=headers)
    return response.json()

# Příklad použití
print(get_account_info())
