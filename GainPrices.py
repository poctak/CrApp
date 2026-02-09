import asyncio
import json
import logging
import time
from collections import deque, defaultdict
from datetime import datetime, timezone
import websockets

# Binance all tickers WebSocket
BINANCE_WS = "wss://stream.binance.com:9443/stream?streams=!ticker@arr"

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Max ticks za 30 minut
# Předpokládáme tick každých 5 sekund → 30*60/5 = 360
MAX_TICKS = 360

# Historie cen
history = defaultdict(lambda: deque(maxlen=MAX_TICKS))

# Spike threshold v procentech
SPIKE_THRESHOLD = 7.0  # 5% nárůst proti průměru

# Funkce pro kontrolu anomálie
def check_anomaly(symbol, price):
    prices = [p for t, p in history[symbol]]
    if not prices:
        return
    avg = sum(prices) / len(prices)
    change = (price - avg) / avg * 100
    if change > SPIKE_THRESHOLD:
        logging.warning(
            f"⚠️ SPIKE DETECTED! {symbol} | Current: {price:.6f} | Avg30min: {avg:.6f} | Change: {change:.2f}%"
        )

async def listen_binance():
    async with websockets.connect(BINANCE_WS, ping_interval=20, ping_timeout=20) as ws:
        logging.info("🚀 Připojeno k Binance WebSocket")
        async for message in ws:
            data = json.loads(message)
            tickers = data["data"]

            timestamp = datetime.now(timezone.utc).isoformat()

            for t in tickers:
                symbol = t["s"]
                # pouze USDT páry
                if not symbol.endswith("USDT"):
                    continue

                price = float(t["c"])   # last price
                # Append do historie
                history[symbol].append((timestamp, price))

                # Kontrola spike
                check_anomaly(symbol, price)

                # Log každou cenu (volitelné, můžeš zakomentovat)
                # logging.info(f"{timestamp} | {symbol:<12} | 💰 {price:.6f}")

async def main():
    while True:
        try:
            await listen_binance()
        except Exception as e:
            logging.error(f"❌ WebSocket error: {e}")
            logging.info("🔄 Reconnect za 5s...")
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
