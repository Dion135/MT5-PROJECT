# model_trainer.py
import numpy as np
from tensorflow.keras.callbacks import EarlyStopping
from model_lstm import build_lstm_model

def train_model(data, n_steps=10):
    """
    Train an LSTM model on historical closing price data.
    
    The model is trained to predict whether the next closing price will be higher
    than the previous one (output 1 for an upward move, 0 for downward).
    
    Parameters:
      data    - DataFrame with a 'close' column.
      n_steps - The number of time steps in each input sequence.
    
    Returns:
      The trained model.
    """
    close_values = data['close'].values
    X, y = [], []
    for i in range(len(close_values) - n_steps):
        seq = close_values[i:i+n_steps]
        # Target: 1 if next closing price is higher than last price in the sequence.
        target = 1 if close_values[i+n_steps] > close_values[i+n_steps-1] else 0
        X.append(seq)
        y.append(target)
    X = np.array(X).reshape((-1, n_steps, 1))
    y = np.array(y)
    
    # Build the LSTM model using our separate module.
    model = build_lstm_model((n_steps, 1))
    
    # Early stopping to prevent overfitting.
    es = EarlyStopping(monitor='loss', patience=5)
    model.fit(X, y, epochs=50, batch_size=16, verbose=1, callbacks=[es])
    
    # Save the model for future prediction use.
    model.save("lstm_model.h5")
    return model

def load_model(path="lstm_model.h5"):
    """Load a pre-trained LSTM model from disk."""
    from tensorflow.keras.models import load_model
    return load_model(path)
