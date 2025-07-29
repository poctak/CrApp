import asyncio
import websockets
import json

# WebSocket URL pro order book (hloubku trhu) BTC/USDT
socket = "wss://stream.binance.com:9443/ws/btcusdt@depth"


async def order_book():
    async with websockets.connect(socket) as websocket:
        print("Připojeno k Binance order book streamu.")
        while True:
            msg = await websocket.recv()
            data = json.loads(msg)

            bids = data.get("b", [])  # nákupní příkazy
            asks = data.get("a", [])  # prodejní příkazy

            print("🔵 Nejvyšší BID:", bids[0] if bids else "Žádné")
            print("🔴 Nejnižší ASK:", asks[0] if asks else "Žádné")
            print("-" * 30)


# Spustit asynchronní smyčku
asyncio.get_event_loop().run_until_complete(order_book())
