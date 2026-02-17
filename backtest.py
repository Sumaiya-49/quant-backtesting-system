import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load Data
data = pd.read_csv("data/stock_data.csv")

# Convert Date column
data['Date'] = pd.to_datetime(data['Date'])
data.set_index('Date', inplace=True)

# Calculate Moving Averages
data['Short_MA'] = data['Close'].rolling(window=20).mean()
data['Long_MA'] = data['Close'].rolling(window=50).mean()

# Generate Signals
data['Signal'] = 0
data['Signal'][20:] = np.where(
    data['Short_MA'][20:] > data['Long_MA'][20:], 1, 0
)

# Calculate Positions
data['Position'] = data['Signal'].diff()

# Calculate Returns
data['Market_Return'] = data['Close'].pct_change()
data['Strategy_Return'] = data['Market_Return'] * data['Signal'].shift(1)

# Performance Metrics
total_return = (1 + data['Strategy_Return']).cumprod()[-1] - 1
max_drawdown = (
    (1 + data['Strategy_Return']).cumprod().cummax() -
    (1 + data['Strategy_Return']).cumprod()
).max()

print("Total Strategy Return: {:.2f}%".format(total_return * 100))
print("Maximum Drawdown: {:.2f}%".format(max_drawdown * 100))

# Plot Equity Curve
(1 + data['Strategy_Return']).cumprod().plot()
plt.title("Equity Curve - Moving Average Strategy")
plt.xlabel("Date")
plt.ylabel("Cumulative Returns")
plt.show()
