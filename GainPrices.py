import asyncio
import requests

async def fetch_last_trade_loop():
    url = "https://api.binance.com/api/v3/trades?symbol=BTCUSDC&limit=1"

    while True:
        try:
            response = requests.get(url)
            data = response.json()
            if data:
                last_trade = data[0]
                price = float(last_trade['price'])
                qty = float(last_trade['qty'])
                print(f"💰 Poslední cena: {price:,.2f} USDC | 📊 Objem: {qty}")
            else:
                print("⚠️ Žádná data")
        except Exception as e:
            print(f"❌ Chyba: {e}")

        await asyncio.sleep(5)

asyncio.run(fetch_last_trade_loop())
