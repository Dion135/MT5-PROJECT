# feature_engineering.py
import pandas as pd
import talib
import MetaTrader5 as mt5

def add_sma(data, period=30):
    """Add a Simple Moving Average (SMA) to the DataFrame."""
    data['sma'] = data['close'].rolling(window=period).mean()
    return data

def add_rsi(data, period=14):
    """Calculate the Relative Strength Index (RSI) and add it as a column."""
    delta = data['close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    data['rsi'] = 100 - (100 / (1 + rs))
    return data
# Calculate Stop Loss and Take Profit dynamically
def calculate_sl_tp(symbol, risk_percentage):
    rates = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M5, 0, 14)
    atr = talib.ATR(rates["high"], rates["low"], rates["close"], timeperiod=14)[-1]
    stop_loss = atr * risk_percentage
    take_profit = stop_loss * 2  # Example: TP is twice the SL
    return stop_loss, take_profit

# Calculate Lot Size dynamically
def calculate_lot_size(account_balance, risk_percentage, stop_loss):
    risk_amount = (account_balance * risk_percentage) / 100
    lot_size = risk_amount / stop_loss
    return round(lot_size, 2)

# Determine Timeframe dynamically
def determine_timeframe(strategy):
    if strategy == "short_term":
        return mt5.TIMEFRAME_M5
    elif strategy == "medium_term":
        return mt5.TIMEFRAME_H1
    else:  # Default to long-term
        return mt5.TIMEFRAME_D1