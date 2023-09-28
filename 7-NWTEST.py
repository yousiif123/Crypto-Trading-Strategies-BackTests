import pandas as pd
import numpy as np
from backtesting import Backtest, Strategy
from scipy.stats import gaussian_kde
from backtesting.lib import crossover

dataframe = pd.read_csv(r'C:\Users\Lenovo\Desktop\algo\BTC.csv')

class NWStrategy(Strategy):
    def init(self):
        self.kernel = gaussian_kde(self.data.Close, bw_method='silverman')

    def next(self):

        close_kde = self.kernel(self.data.Close)
        kernel_ma = np.convolve(close_kde, np.ones(20) / 20, mode='same')

        upper_env = kernel_ma + 0.5 * np.std(close_kde)
        lower_env = kernel_ma - 0.5 * np.std(close_kde)
        if crossover(close_kde, upper_env):
            self.buy()
        elif crossover(lower_env, close_kde):
            self.sell()


dataframe['Timestamp'] = pd.to_datetime(dataframe['Timestamp'])
dataframe.set_index('Timestamp', inplace=True)
bt = Backtest(dataframe, NWStrategy, cash=1000000)
results = bt.run()
print(results)