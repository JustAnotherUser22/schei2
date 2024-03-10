
from ta.trend import EMAIndicator
import pandas as pd
import matplotlib.pyplot as plt


def main():
   filePath = "D:\script\schei2\supAndRes\DAT_ASCII_EURUSD_T_2022_onlyFebruary.csv"
   f = pd.read_csv(filePath)
   close = f.iloc[:,1]
   #close = close[0:1000000]
   #close = close[1:100]
   #close = close[1:63897]  #1 giorno
   #close = close[63898 : 119401]  #secondo giorno
   close = close[0 : 119401]  #secondo giorno

   params = EMAIndicator(close = close, window = 20000)
   ema1 = params.ema_indicator()

   params = EMAIndicator(close = close, window = 10000)
   ema2 = params.ema_indicator()


   plt.plot(close, color = 'red')
   plt.plot(ema1, color = 'black')
   plt.plot(ema2, color = 'blue')

   plt.show()

   


if __name__ == "__main__":
   main()