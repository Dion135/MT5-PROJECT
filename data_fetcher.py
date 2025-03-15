# data_fetcher.py
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

def initialize_mt5(config):
    """Initialize MT5 connection using configuration settings."""
    if not mt5.initialize(
        config['meta_trader']['terminal_path'],
        login=config['meta_trader']['login'],
        password=config['meta_trader']['password'],
        server=config['meta_trader']['server']
    ):
        print("initialize() failed, error code =", mt5.last_error())
        return False
    return True

def shutdown_mt5():
    """Shut down the MetaTrader 5 connection."""
    mt5.shutdown()

def fetch_data(symbol, timeframe, count):
    """
    Fetch a specified number of historical candles for the given symbol.
    
    Parameters:
      symbol   - Trading symbol as a string.
      timeframe- Timeframe identifier, e.g., "TIMEFRAME_M1".
      count    - Number of candles to fetch.
    
    Returns:
      A pandas DataFrame of rates.
    """
    timeframe_map = {
        "TIMEFRAME_M1": mt5.TIMEFRAME_M1,
        "TIMEFRAME_M5": mt5.TIMEFRAME_M5,
        "TIMEFRAME_M15": mt5.TIMEFRAME_M15,
        "TIMEFRAME_H1": mt5.TIMEFRAME_H1,
        # Add additional mappings as needed.
    }
    timeframe_const = timeframe_map.get(timeframe, mt5.TIMEFRAME_M1)
    
    utc_from = datetime.now() - pd.Timedelta(minutes=count)
    rates = mt5.copy_rates_from(symbol, timeframe_const, utc_from, count)
    if rates is None:
        print("No data received for symbol:", symbol)
        return pd.DataFrame()
    data = pd.DataFrame(rates)
    data['time'] = pd.to_datetime(data['time'], unit='s')
    return data
