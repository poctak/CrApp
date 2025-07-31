from binance.client import Client
from binance.streams import ThreadedWebsocketManager

def handle_msg(msg):
    price = msg['p']
    qty = msg['q']
    print(f"💰 Cena: {price} | 📊 Objem: {qty}")

twm = ThreadedWebsocketManager()
twm.start()

# Naslouchá obchodům na páru BTCUSDC
twm.start_trade_socket(callback=handle_msg, symbol='BTCUSDC')
