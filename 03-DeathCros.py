from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import talib as ta

df = pd.read_csv(r'C:\Users\Lenovo\Desktop\algo\BTC_01_01_21_to_01_01_22.csv')

class DeathCross(Strategy):
    def init(posi):
        close_series = posi.data.Close.to_series()

        posi.sma_20 = posi.I(ta.SMA, close_series, 20)
        posi.sma_50 = posi.I(ta.SMA, close_series, 50)

    def next(posi):
        if(crossover(posi.sma_50, posi.sma_20) and posi.position):
            posi.buy(size=1)
        elif(crossover(posi.sma_20, posi.sma_50)):
            posi.buy(size=-1)   
        return
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp', inplace=True) 
df = (df / 1e6).assign(Volume=df.Volume * 1e6)

backtest = Backtest(df, DeathCross)
result=backtest.run()
print(result)
#backtest.plot()
