import asyncio
import json
import logging
import websockets
from datetime import datetime, timezone

BINANCE_WS = "wss://stream.binance.com:9443/stream?streams=!ticker@arr"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


async def listen_binance():
    async with websockets.connect(
        BINANCE_WS,
        ping_interval=20,
        ping_timeout=20
    ) as ws:
        logging.info("🚀 Připojeno k Binance WebSocket")

        async for message in ws:
            data = json.loads(message)

            # pole všech tickerů
            tickers = data["data"]

            timestamp = datetime.now(timezone.utc).isoformat()

            for t in tickers:
                symbol = t["s"]

                # pouze USDT páry
                if not symbol.endswith("USDT"):
                    continue

                price = float(t["c"])   # last price
                volume = float(t["v"])  # base volume

                logging.info(
                    f"{timestamp} | {symbol:<12} | 💰 {price:,.6f} | 📊 {volume:,.2f}"
                )


async def main():
    while True:
        try:
            await listen_binance()
        except Exception as e:
            logging.error(f"❌ WebSocket chyba: {e}")
            logging.info("🔄 Reconnect za 5s...")
            await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
