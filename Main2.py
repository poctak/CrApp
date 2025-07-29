import asyncio
import websockets
import json
import time

socket = "wss://stream.binance.com:9443/ws/btcusdt@depth"

# Ukládáme order book do proměnné
order_book_state = {
    "bids": [],
    "asks": []
}


# Formátované vypsání top 5 úrovní
def print_order_book():
    bids = order_book_state["bids"][:5]
    asks = order_book_state["asks"][:5]

    print("\n📘 ORDER BOOK – BTC/USDT")
    print(f"{'ASK (Cena)':>12} {'Množství':>10}     {'BID (Cena)':>12} {'Množství':>10}")
    print("-" * 50)
    for i in range(max(len(asks), len(bids))):
        ask_price, ask_qty = asks[i] if i < len(asks) else ("", "")
        bid_price, bid_qty = bids[i] if i < len(bids) else ("", "")
        print(f"{ask_price:>12} {ask_qty:>10}     {bid_price:>12} {bid_qty:>10}")
    print("-" * 50)


async def listen_order_book():
    async with websockets.connect(socket) as websocket:
        print("🔌 Připojeno k Binance WebSocket (BTCUSDT order book)")
        last_print = time.time()
        while True:
            msg = await websocket.recv()
            data = json.loads(msg)

            # Update bid/ask seznamu
            order_book_state["bids"] = data.get("b", [])
            order_book_state["asks"] = data.get("a", [])

            # Vypiš každé 2 sekundy
            if time.time() - last_print > 2:
                print_order_book()
                last_print = time.time()


asyncio.get_event_loop().run_until_complete(listen_order_book())
