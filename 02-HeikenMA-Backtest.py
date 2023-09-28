from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd

class HeikenMAStrategy(Strategy):
    def init(posi):
        posi.ema_1 = 30
        posi.ema_2 = 50
        posi.stop_loss = 0.05  # stop-loss at 5%

    def next(posi):
        close_prices = posi.data.Close

        if len(close_prices) < posi.ema_2:
            return
        ema1 = close_prices[-posi.ema_1:].mean()
        ema2 = close_prices[-posi.ema_2:].mean()

        #Close
        ha_close = (posi.data.Open[-1] + posi.data.High[-1] + posi.data.Low[-1] + close_prices[-1]) / 4

        if not posi.position:

            if ema1 > ema2 and ha_close > ema1:
                posi.buy()  # Enter
                posi.stop_loss_level = close_prices[-1] * (1 - posi.stop_loss)
        else:

            if ema1 < ema2 and ha_close < ema1:
                posi.sell()  # Exit
            elif close_prices[-1] <= posi.stop_loss_level:
                posi.sell()  # Stop-loss

df = pd.read_csv(r'C:\Users\Lenovo\Desktop\algo\D.csv')

#Time frame optimize
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp', inplace=True)

backtest = Backtest(df, HeikenMAStrategy)
result=backtest.run()
print(result)

backtest.plot() #Visual Plot