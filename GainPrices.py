import asyncio
import requests
import logging
from datetime import datetime, timezone
from elasticsearch import Elasticsearch

# Nastavení logování
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)


# Elasticsearch client
es = Elasticsearch("http://localhost:9200")  # uprav pokud máš jinou adresu
INDEX_NAME = "my-crypto-index"
async def fetch_last_trade_loop():
    url = "https://api.binance.com/api/v3/trades?symbol=BTCUSDC&limit=1"

    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()  # ošetří chyby HTTP
            data = response.json()
            if data:
                last_trade = data[0]
                price = float(last_trade['price'])
                qty = float(last_trade['qty'])
                timestamp = datetime.now(timezone.utc).isoformat()

                # Vložení do Elasticsearch
                doc_price = {
                    "pair": "BTCUSDC",
                    "timestamp": timestamp,
                    "title": "price",
                    "value": price
                }
                doc_qty = {
                    "pair": "BTCUSDC",
                    "timestamp": timestamp,
                    "title": "quantity",
                    "value": qty
                }

                es.index(index=INDEX_NAME, document=doc_price)
                es.index(index=INDEX_NAME, document=doc_qty)

                logging.info(f"💰 Poslední cena: {price:,.2f} USDC | 📊 Objem: {qty}")
            else:
                logging.warning("⚠️ Žádná data")
        except Exception as e:
            logging.error(f"❌ Chyba: {e}")

        await asyncio.sleep(5)

if __name__ == "__main__":
    logging.info("🚀 Spouštím sledování BTC/USDC...")
    asyncio.run(fetch_last_trade_loop())
