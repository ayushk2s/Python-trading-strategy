import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_ta as ta  # Using pandas_ta instead of TA-Lib

# Load CSV data
data = pd.read_csv("D:/Python Backtest/DOGEUSDT3m.csv", parse_dates=["Date"], index_col="Date")

# Strategy Parameters (adjusted for more signal generation)
fast_length = 5
slow_length = 15
trend_length = 30
rsi_length = 10
rsi_overbought = 70    # slightly lower than before
rsi_oversold = 30      # slightly higher than before
macd_fast_length = 8
macd_slow_length = 17
macd_signal_length = 9
atr_length = 10
adx_length = 14
adx_threshold = 20     # lowered threshold to allow more trending periods
profit_factor = 2.0    # profit target multiplier for ATR
atr_multiplier = 1.5   # stop loss multiplier for ATR
initial_cash = 100

# Calculate Indicators using pandas_ta
data["Fast_EMA"] = ta.ema(data["Close"], length=fast_length)
data["Slow_EMA"] = ta.ema(data["Close"], length=slow_length)
data["Trend_SMA"] = ta.sma(data["Close"], length=trend_length)
data["RSI"] = ta.rsi(data["Close"], length=rsi_length)

# Calculate MACD and extract appropriate columns
macd = ta.macd(data["Close"], fast=macd_fast_length, slow=macd_slow_length, signal=macd_signal_length)
print("MACD Columns:", macd.columns)
data["MACD"] = macd["MACD_8_17_9"]
data["MACD_Signal"] = macd["MACDs_8_17_9"]

data["ATR"] = ta.atr(data["High"], data["Low"], data["Close"], length=atr_length)
data["ADX"] = ta.adx(data["High"], data["Low"], data["Close"], length=adx_length)["ADX_14"]

# Drop rows with NaN values (from indicator calculations)
data.dropna(inplace=True)

# --- Signal Generation using Count-Based Approach ---
# Instead of requiring every condition to be true, we count signals:
data["bull_count"] = ((data["Fast_EMA"] > data["Slow_EMA"]).astype(int) +
                      (data["RSI"] < rsi_oversold).astype(int) +
                      (data["MACD"] > data["MACD_Signal"]).astype(int))
data["bear_count"] = ((data["Fast_EMA"] < data["Slow_EMA"]).astype(int) +
                      (data["RSI"] > rsi_overbought).astype(int) +
                      (data["MACD"] < data["MACD_Signal"]).astype(int))

# Apply ADX filter and require at least 2 signals for an entry:
data["Bullish"] = (data["bull_count"] >= 2) & (data["ADX"] > adx_threshold)
data["Bearish"] = (data["bear_count"] >= 2) & (data["ADX"] > adx_threshold)

print(f"Total Bullish Signals: {data['Bullish'].sum()}")
print(f"Total Bearish Signals: {data['Bearish'].sum()}")

if data["Bullish"].sum() == 0 and data["Bearish"].sum() == 0:
    print("No Buy/Sell signals found. Consider adjusting your parameters further.")

# --- Trade Simulation with Risk Management ---
trade_open = False
position = 0  # 1 for long, -1 for short
entry_price = 0.0
stop_loss = 0.0
take_profit = 0.0
trade_entry_time = None
results = []

for dt, row in data.iterrows():
    if not trade_open:
        # Enter a trade if a bullish or bearish signal is triggered:
        if row["Bullish"]:
            trade_open = True
            position = 1
            entry_price = row["Close"]
            stop_loss = entry_price - row["ATR"] * atr_multiplier
            take_profit = entry_price + row["ATR"] * profit_factor
            trade_entry_time = dt
        elif row["Bearish"]:
            trade_open = True
            position = -1
            entry_price = row["Close"]
            stop_loss = entry_price + row["ATR"] * atr_multiplier
            take_profit = entry_price - row["ATR"] * profit_factor
            trade_entry_time = dt
    else:
        exit_trade = False
        exit_reason = ""
        exit_price = row["Close"]
        # For long positions:
        if position == 1:
            if row["Low"] <= stop_loss:
                exit_trade = True
                exit_price = stop_loss
                exit_reason = "Stop Loss Hit"
            elif row["High"] >= take_profit:
                exit_trade = True
                exit_price = take_profit
                exit_reason = "Take Profit Hit"
            elif row["Bearish"]:
                exit_trade = True
                exit_reason = "Bearish Signal Exit"
        # For short positions:
        elif position == -1:
            if row["High"] >= stop_loss:
                exit_trade = True
                exit_price = stop_loss
                exit_reason = "Stop Loss Hit"
            elif row["Low"] <= take_profit:
                exit_trade = True
                exit_price = take_profit
                exit_reason = "Take Profit Hit"
            elif row["Bullish"]:
                exit_trade = True
                exit_reason = "Bullish Signal Exit"

        if exit_trade:
            # Calculate trade return:
            if position == 1:
                trade_return = (exit_price - entry_price) / entry_price
            else:
                trade_return = (entry_price - exit_price) / entry_price
            results.append({
                'Entry_Time': trade_entry_time,
                'Exit_Time': dt,
                'Position': position,
                'Entry_Price': entry_price,
                'Exit_Price': exit_price,
                'Return': trade_return,
                'Exit_Reason': exit_reason
            })
            trade_open = False
            position = 0

# If a trade is still open at the end, exit at the final price:
if trade_open:
    final_price = data.iloc[-1]["Close"]
    if position == 1:
        trade_return = (final_price - entry_price) / entry_price
    else:
        trade_return = (entry_price - final_price) / entry_price
    results.append({
        'Entry_Time': trade_entry_time,
        'Exit_Time': data.index[-1],
        'Position': position,
        'Entry_Price': entry_price,
        'Exit_Price': final_price,
        'Return': trade_return,
        'Exit_Reason': 'Final Bar Exit'
    })

# Convert trade results to DataFrame
trades = pd.DataFrame(results)
if trades.empty:
    print("No trades were executed. Please review the signal generation parameters.")
else:
    trades["Cumulative_Return"] = (1 + trades["Return"]).cumprod() * initial_cash
    print(trades)

    # Plot cumulative profit of the strategy based on simulated trades
    plt.figure(figsize=(12,6))
    plt.plot(trades["Exit_Time"], trades["Cumulative_Return"], marker="o", linestyle="-", color="blue")
    plt.title("Cumulative Profit Over Trades")
    plt.xlabel("Exit Time")
    plt.ylabel("Cumulative Profit ($)")
    plt.grid(True)
    plt.show()

# Plot buy/sell points on the price chart for visual reference
plt.figure(figsize=(12,6))
plt.plot(data.index, data["Close"], label="Price", color="black")
# Mark entry points
if not trades.empty:
    for idx, trade in trades.iterrows():
        entry = trade["Entry_Time"]
        exit_time = trade["Exit_Time"]
        pos = trade["Position"]
        color = "green" if pos == 1 else "red"
        plt.scatter(entry, data.loc[entry, "Close"], marker="^" if pos==1 else "v", color=color, s=100, label="Entry" if idx==0 else "")
        plt.scatter(exit_time, data.loc[exit_time, "Close"], marker="o", color="blue", s=100, label="Exit" if idx==0 else "")
plt.title("Trade Entries and Exits on Price Chart")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.show()
