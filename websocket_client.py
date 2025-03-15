# websocket_client.py
import time
import MetaTrader5 as mt5

def run_realtime_listener(symbol, callback, polling_interval=1):
    """
    Poll for real-time tick data and pass it to the provided callback.
    
    Parameters:
      symbol           - Trading symbol.
      callback(tick)   - Function to handle each tick.
      polling_interval - Interval in seconds between polling.
    """
    print("Starting realtime listener for:", symbol)
    while True:
        tick = mt5.symbol_info_tick(symbol)
        if tick is not None:
            callback(tick)
        time.sleep(polling_interval)
