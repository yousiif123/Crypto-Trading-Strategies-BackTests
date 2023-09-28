from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA
import pandas as pd
import numpy as np


class BollingerBandRSIStrategy(Strategy):
    n = 20  # Number of periods for moving average
    k = 2  # Number of standard deviations to use for Bollinger Bands
    rsi_n = 14  # Number of periods to use for RSI calculation
    rsi_overbought = 70  # RSI level to signal overbought conditions
    stop_loss_pct = 0.02  # Stop-loss percentage threshold

    def init(self):
        # Calculate moving average and standard deviation of the close prices
        ma = self.I(np.nanmean, self.data.Close[-self.n:])
        std = self.I(np.nanstd, self.data.Close[-self.n:])

        # Calculate upper and lower Bollinger Bands
        upper_band = ma + self.k * std
        lower_band = ma - self.k * std

        # Calculate Relative Strength Index
        delta = upper_band - lower_band
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(self.rsi_n).mean()
        avg_loss = loss.rolling(self.rsi_n).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - 100 / (1 + rs)

        # Define entry and exit signals
        self.buy_signal = (self.data.Close[-1] <= lower_band[-1]) & (rsi[-1] < self.rsi_overbought)
        self.sell_signal = (self.data.Close[-1] >= upper_band[-1]) | (rsi[-1] >= self.rsi_overbought)
        self.stop_loss = self.data.Low.min() * (1 - self.stop_loss_pct)

    def next(self):
        # Check if we already have an open position
        if self.position:
            # Check for exit signals
            if self.sell_signal:
                self.sell()
            elif self.data.Low[-1] <= self.stop_loss:
                self.sell()

            # Update stop-loss threshold
            self.stop_loss = max(self.data.Low[-1], self.stop_loss)

        elif self.buy_signal:
            # Enter a new long position at the current market price
            self.buy()
            self.stop_loss = self.data.Low[-1] * (1 - self.stop_loss_pct)

data = pd.read_csv(r'C:\Users\Lenovo\Desktop\algo\BTC.csv', index_col='Timestamp', parse_dates=True)


bt = Backtest(data, BollingerBandRSIStrategy, cash=100000, commission=0.002)
stats = bt.run()
print(stats)