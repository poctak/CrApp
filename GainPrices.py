import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

async def stream_price():
    url = "wss://stream.binance.com:9443/ws/btcusdc@trade"
    logging.info("📡 Připojuji se ke streamu BTC/USDC...")
    try:
        async with websockets.connect(url) as websocket:
            while True:
                msg = await websocket.recv()
                data = json.loads(msg)
                price = data['p']
                quantity = data['q']
                logging.info(f"💰 Cena: {price} | 📊 Objem: {quantity}")
                await asyncio.sleep(10)
    except Exception as e:
        logging.error(f"❌ Chyba při připojení: {e}")

if __name__ == "__main__":
    asyncio.run(stream_price())
