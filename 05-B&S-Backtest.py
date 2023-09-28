from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import talib as ta
data = pd.read_csv(r'C:\Users\Lenovo\Desktop\algo\BTC.csv')

class BBandsAndStochastic(Strategy):
    def init(self):
        high_series = self.data.High.to_series()
        low_series = self.data.Low.to_series()
        close_series = self.data.Close.to_series()

        self.bbands = self.I(ta.BBANDS, close_series, name='BB')
        self.stochastic = self.I(ta.STOCH, high_series, low_series, close_series, name='S')

    def next(self):
        BBandsStatus = BollingerStatus(self.bbands, self.data.High, self.data.Low)

        if self.position:
            if (self.position.is_long and BBandsStatus == HitUB) or (self.position.is_short and BBandsStatus == HitLB):
                self.position.close()
        else:
            StochStatus = StochasticStatus(self.stochastic)

            if BBandsStatus == HitLB and StochStatus == Overs:
                self.buy(size=1) # Long
            elif BBandsStatus == HitUB and StochStatus == Overb:
                self.buy(size=-1) # Short
                return

Overs = 1
Overb = 2
HitLB = 1
HitUB = 2

def StochasticStatus(stochastic):
    if stochastic[0][-1] < 10 and stochastic[1][-1] < 50:
        return Overs
    elif stochastic[0][-1] > 20 and stochastic[1][-1] > 90:
        return Overb
    return None
    
def BollingerStatus(bollinger, high, low):
    if low[-1] <= bollinger[2][-1]:
        return HitLB
    elif high[-1] >= bollinger[0][-1]:
        return HitUB
    return None

data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)

backtest = Backtest(data, BBandsAndStochastic, cash=100000)
result=backtest.run()
print(result)
#backtest.plot()