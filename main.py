import os
import time
import MetaTrader5 as mt5
import yaml
from data_fetcher import initialize_mt5, shutdown_mt5, fetch_data
from feature_engineering import add_sma, add_rsi, calculate_sl_tp, calculate_lot_size, determine_timeframe
from predictor import predict_signal, predict_signal_ml
from model_trainer import train_model, load_model

# Load configuration
if not os.path.exists("config.yaml"):
    print("Configuration file 'config.yaml' not found. Ensure it exists in the project directory.")
    quit()

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

bot_settings = config.get("bot", {})
symbol = bot_settings.get("symbol")
strategy = bot_settings.get("strategy")
risk_percentage = bot_settings.get("risk_percentage")

# Ensure MetaTrader 5 initialization
if not mt5.initialize():
    print("MetaTrader 5 initialization failed. Please check your MetaTrader setup.")
    quit()

# Check if symbol is selected
if not mt5.symbol_select(symbol, True):
    print(f"Failed to select symbol: {symbol}. Ensure it's available in MetaTrader.")
    mt5.shutdown()
    quit()

# Determine dynamic parameters
timeframe = determine_timeframe(strategy)
if not timeframe:
    print(f"Invalid strategy provided: {strategy}. Unable to determine timeframe.")
    mt5.shutdown()
    quit()

stop_loss, take_profit = calculate_sl_tp(symbol, risk_percentage)
account_info = mt5.account_info()
if not account_info:
    print("Failed to retrieve account information. Ensure your MetaTrader account is logged in.")
    mt5.shutdown()
    quit()

account_balance = account_info.balance
lot_size = calculate_lot_size(account_balance, risk_percentage, stop_loss)

# Trading function
def place_trade():
    rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 1)
    if not rates or len(rates) == 0:
        print("Failed to fetch rates for the symbol. Ensure the symbol data is available.")
        return

    price = rates[0]["close"]

    # Create trade request
    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_BUY,
        "price": price,
        "sl": price - stop_loss,
        "tp": price + take_profit,
        "deviation": 10,
        "magic": 123456,
        "comment": "Automated Trade"
    }

    # Send trade request
    result = mt5.order_send(request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"Trade failed. Error code: {result.retcode}.")
    else:
        print("Trade successfully executed:", result)

# Main function
def main():
    try:
        # Execute the trade
        place_trade()
    finally:
        # Shutdown MetaTrader 5 after execution
        mt5.shutdown()

# Check for existing open positions before placing a new order
if __name__ == "__main__":
    main()
