from binance.client import Client
import os
import time
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('BINANCE_API_KEY')
api_secret = os.getenv('BINANCE_API_SECRET')

client = Client(api_key, api_secret, testnet=True)

try:
    print("Pinging Binance Futures Testnet...")
    client.futures_ping()
    print("Ping successful!")

    print("Fetching server time...")
    server_time = client.futures_time()['serverTime']
    local_time = int(time.time() * 1000)
    print(f"Server time: {server_time}")
    print(f"Local time:  {local_time}")
    print(f"Difference:  {server_time - local_time} ms")

    print("Testing API keys with futures_account()...")
    account = client.futures_account()
    print("Keys are valid! Account balance:", account.get('totalWalletBalance'))

except Exception as e:
    print(f"ERROR: {e}")
