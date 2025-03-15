# predictor.py
import numpy as np

def predict_signal(data):
    """
    Generate a trading signal using a simple rule:
      - "buy" if the last close is above the SMA,
      - "sell" if below,
      - "hold" otherwise.
    """
    if data.empty or 'sma' not in data.columns:
        return None

    last_row = data.iloc[-1]
    if last_row['close'] > last_row['sma']:
        return "buy"
    elif last_row['close'] < last_row['sma']:
        return "sell"
    else:
        return "hold"

def predict_signal_ml(data, model, n_steps=10):
    """
    Use the trained LSTM model to predict the next price movement.
    
    Returns "buy" if the predicted probability exceeds 0.5, otherwise "sell".
    """
    close_values = data['close'].values
    if len(close_values) < n_steps:
        return None
    last_sequence = close_values[-n_steps:]
    X_input = np.array(last_sequence).reshape((1, n_steps, 1))
    prob = model.predict(X_input)[0][0]
    return "buy" if prob > 0.5 else "sell"
