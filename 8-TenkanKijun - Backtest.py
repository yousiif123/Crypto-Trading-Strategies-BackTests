from backtesting import Backtest, Strategy
import pandas as pd
data = pd.read_csv(r'C:\Users\Lenovo\Desktop\algo\BTC.csv')

def tenkan(high, low, periot=9):
    if(len(high) != len(low)):
        raise Exception('Invalid')

    tenkan_values = []
    for i in range(periot-1):
        tenkan_values.append(None)
    for tick in range(periot, len(high)+1):
        hp = high[tick-periot: tick]
        lp = low[tick-periot: tick]
        h_max = max(hp)
        l_min = min(lp)
        tenkan = (h_max + l_min) / 2
        tenkan_values.append(tenkan)
    return pd.Series(tenkan_values)

def FindFDP(line1, line2):
    for i in range(len(line1)-1, -1, -1):
        if(line1[i] != line2[i]):
            return i
    return None

def isCrossing(line1, line2):
    _line1 = line1[:len(line1)-1]
    _line2 = line2[:len(line2)-1]

    fdp = FindFDP(_line1, _line2)
    if(fdp == None):
        return False

    if(line1[-1] > line2[-1] and _line1[fdp] < _line2[fdp]):
        return True

    return False

def ichimoku_kijun(high, low, periot=26):
    if(len(high) != len(low)):
        raise Exception('Invalid')
    kijun_values = []
    for i in range(periot-1):
        kijun_values.append(None)
    kijun_range = range(periot, len(high)+1)

    for tick in kijun_range:
        hp = high[tick-periot: tick]
        lp = low[tick-periot: tick]
        h_max = max(hp)
        l_min = min(lp)
        kijun = (h_max + l_min) / 2
        kijun_values.append(kijun)
    return pd.Series(kijun_values)

class TenkanKijun(Strategy):
    def init(self):
        high_series = self.data.High.to_series()
        low_series = self.data.Low.to_series()

        self.tenkan = self.I(tenkan, high_series, low_series, name='Tenkan')
        self.ichimoku_kijun = self.I(ichimoku_kijun, high_series, low_series, name='Kijun')

    def next(self):
        if self.position:
            if isCrossing(self.ichimoku_kijun, self.tenkan):
                self.position.close()
        else:
            if(isCrossing(self.tenkan, self.ichimoku_kijun)):
                self.buy()

data['Timestamp'] = pd.to_datetime(data['Timestamp'])
data.set_index('Timestamp', inplace=True)
backtest = Backtest(data, TenkanKijun)
result=backtest.run()
print(result)
#backtest.plot()