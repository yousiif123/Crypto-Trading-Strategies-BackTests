import backtesting
from backtesting import Backtest, Strategy
from backtesting.lib import SignalStrategy
import pandas as pd

df = pd.read_csv(r'C:\Users\Lenovo\Desktop\algo\BTC.csv')

class GridStrategy(SignalStrategy):
    def init(posi):
        posi.grid_size = 100
        posi.grid_levels = 10
        posi.current_level = 0
        
    def next(self):
        if len(self.data) > 0:
            if self.current_level <= self.grid_levels:
                if self.position.size == 0:
                    # Calculate price levels for grid
                    price = self.data.Close[0]
                    upper_price = price + (self.grid_size * self.current_level)
                    lower_price = price - (self.grid_size * self.current_level)

                    #Orders
                    if price==upper_price:
                        self.buy()
                    if price==lower_price:
                        self.buy()
                    self.current_level += 1

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp', inplace=True)

bt = Backtest(df, GridStrategy)
result = bt.run()
print(result)
df.plot()