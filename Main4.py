import asyncio
import websockets
import json

socket = "wss://stream.binance.com:9443/ws/pepeeur@trade"

async def print_trades():
    async with websockets.connect(socket) as websocket:
        print("📡 Připojeno na živé obchody (BTCUSDT)")
        while True:
            msg = await websocket.recv()
            data = json.loads(msg)
            price = data['p']
            quantity = data['q']
            side = 'SELL' if data['m'] else 'BUY'
            print(f"{side} | Cena: {price} | Množství: {quantity}")

asyncio.get_event_loop().run_until_complete(print_trades())
