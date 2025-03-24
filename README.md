# Python-trading-strategy
This is python written code, for backtesting a trading strategy. Do not use in real without knowing in depth about it. 


Trading Strategy Backtest using pandas_ta

This repository contains a Python script that implements a trading strategy backtest using pandas_ta for technical indicator calculations. The strategy is applied to historical cryptocurrency price data from a CSV file.

Features

Uses Exponential Moving Averages (EMA) to detect trends.

Implements RSI (Relative Strength Index) for momentum analysis.

Uses MACD (Moving Average Convergence Divergence) for trend confirmation.

Includes ATR (Average True Range) for stop-loss and take-profit levels.

ADX (Average Directional Index) is used to filter trending markets.

Trade execution logic based on signal count approach.

Risk management with stop-loss and take-profit orders.

Backtest results are visualized with cumulative profit and trade markers on price charts.

Installation

# pip install pandas numpy matplotlib pandas_ta

Ensure you have Python installed along with the following dependencies:

pip install pandas numpy matplotlib pandas_ta

# Usage

Place your CSV file (e.g., DOGEUSDT3m.csv) in the specified directory.

Update the script to load the correct CSV file.

Run the script:

# python backtest.py

python backtest.py

The script will:

Load historical price data.

Calculate technical indicators.

Generate buy/sell signals based on predefined conditions.

Simulate trades and track performance.

Plot the cumulative profit graph.

Visualize trade entries and exits on the price chart.

Parameters

You can adjust the strategy parameters in the script:

fast_length = 5
slow_length = 15
trend_length = 30
rsi_length = 10
rsi_overbought = 70
rsi_oversold = 30
macd_fast_length = 8
macd_slow_length = 17
macd_signal_length = 9
atr_length = 10
adx_length = 14
adx_threshold = 20
profit_factor = 2.0
atr_multiplier = 1.5
initial_cash = 100

Modifying these parameters allows you to fine-tune the strategy for different market conditions.

Output

The script prints the total number of bullish and bearish signals.

If no signals are generated, it suggests adjusting parameters.

A summary of all executed trades is displayed, including entry/exit prices, returns, and reasons for exit.

A cumulative profit chart is generated.

Buy/sell markers are plotted on the price chart for reference.

Example Trade Output

Total Bullish Signals: 15
Total Bearish Signals: 12
+------------+------------+----------+--------------+--------------+--------+----------------+
| Entry_Time | Exit_Time  | Position | Entry_Price  | Exit_Price   | Return | Exit_Reason   |
+------------+------------+----------+--------------+--------------+--------+----------------+
| 2024-03-01 | 2024-03-02 |   1      | 0.075       | 0.078        | 4.0%   | Take Profit Hit |
+------------+------------+----------+--------------+--------------+--------+----------------+

Visualization

Cumulative profit over time:


Trade entries and exits plotted on price chart:


Contribution

Feel free to modify and improve the script. If you encounter any issues or have suggestions, create a pull request or open an issue.

Disclaimer

This project is for educational and research purposes only. Trading involves risks, and past performance is not indicative of future results. Use this strategy at your own discretion.

