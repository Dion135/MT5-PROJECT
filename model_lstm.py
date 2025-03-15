import MetaTrader5 as mt5
import pandas as pd
import yaml
from requests import get_market_data, calculate_atr  # Import from your requests.py
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

def build_lstm_model(input_shape):
    """
    Build and compile an LSTM model for binary classification.
    
    Parameters:
      input_shape - Tuple specifying the shape of the input (n_steps, n_features)
    
    Returns:
      A compiled Keras model.
    """
    model = Sequential([
        LSTM(50, activation='relu', input_shape=input_shape),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model
def get_dynamic_config(symbol, current_price):
    """Calculates dynamic config parameters based on MT5 data."""

    atr = calculate_atr(symbol, "1m", 500)  # Calculate ATR on 1-minute timeframe

    if atr is None:
        return None

    # Timeframe Selection (Example Logic):
    if atr > 0.0005:  # High volatility
        timeframe = "5m"
    else:
        timeframe = "15m"

    # Lot Size Calculation (Example Logic):
    lot = 0.1  # Base lot size
    lot_multiplier = atr * 100000  # Adjust based on ATR
    lot += lot_multiplier
    lot = round(lot, 2)  # Round to 2 decimal places

    # Stop-Loss and Take-Profit Calculation (Example Logic):
    stop_loss = round(current_price - (1.5 * atr), 5)  # 1.5 ATR below
    take_profit = round(current_price + (2 * atr), 5)  # 2 ATR above

    return {
        "timeframe": timeframe,
        "lot": lot,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
    }