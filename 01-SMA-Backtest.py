from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import talib

class SMAScalpingStrategy(Strategy):
    def init(self):
        #15 and 25 period simple moving averages
        self.sma15 = self.I(talib.SMA, self.data.Close,15)
        self.sma25 = self.I(talib.SMA, self.data.Close,25)

    def next(self):
        # Enters a long position If 15 period SMA cross above 25 period SMA
        if crossover(self.sma15, self.sma25):
            self.buy()
        # Exit long position If 15 period SMA cross below 25 period SMA 
        elif crossover(self.sma25, self.sma15):
            self.sell()

# Load Data
data = pd.read_csv('D:/BTC/btc_data.csv')

# Convert to datetime object
data['Timestamp'] = pd.to_datetime(data['Timestamp'])

# change DataFrame index to timestamp
data.set_index('Timestamp', inplace=True)


# Create a Backtest object with data
bt = Backtest(data, SMAScalpingStrategy, cash=100000, commission=0.02)

# Run the backtest
output = bt.run()
print(output)

# Display the results
bt.plot()
