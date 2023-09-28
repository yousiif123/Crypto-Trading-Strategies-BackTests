from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import talib as tal
df = pd.read_csv(r'C:\Users\Lenovo\Desktop\algo\BTC.csv')

class GoldenX(Strategy):
    def init(posi):
        close_series = posi.data.Close.to_series()

        posi.sma_30 = posi.I(tal.SMA, close_series, 30)
        posi.sma_50 = posi.I(tal.SMA, close_series, 50)

    def next(posi):
        if(crossover(posi.sma_50, posi.sma_30) and posi.position):
            posi.buy(size=-1)
        elif(crossover(posi.sma_30, posi.sma_50)):
            posi.buy(size=1)
            
        return

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp', inplace=True)
bt = Backtest(df, GoldenX, cash=100000, commission=0.02)
result=bt.run()
print(result)
bt.plot()
