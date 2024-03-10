
from ta.trend import MACD
from ta.trend import EMAIndicator
from ta.trend import SMAIndicator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
   filePath = "D:\script\schei2\supAndRes\DAT_ASCII_EURUSD_T_2022_onlyFebruary.csv"
   f = pd.read_csv(filePath)
   close = f.iloc[:,1]
   #close = close[1:100]
   #close = close[1:63897]  #1 giorno
   #close = close[63898 : 119401]  #secondo giorno
   close = close[0 : 119401]  #secondo giorno

   #params = MACD(close = close, window_slow=26, window_fast=12, window_sign=9)
   params = MACD(close = close, window_slow = 20000, window_fast = 10000, window_sign = 22)
   macd = params.macd()
   signal = params.macd_signal()
   histogram = params.macd_diff()
   zeroLine = [0] * len(close)

   figure, axis = plt.subplots(2) 

   range = [-10, 119401]

   axis[0].plot(close, label = "close")
   axis[0].legend()
   axis[0].set_xlim(range)

   derivative = np.gradient(signal)
   derivative = pd.DataFrame(derivative, columns = ['values'])
   derivative = derivative.loc[:, 'values']
   
   derivativeAverage = SMAIndicator(close = derivative, window = 10000)
   derivativeAverage = derivativeAverage.sma_indicator()
   derivative = derivativeAverage

   #axis[1].plot(macd, 'b', label = "macd")
   #axis[1].plot(signal, 'r', label = "signal")
   axis[1].plot(derivative, 'r', label = "signal")
   axis[0].plot(params._emafast, 'b', label = "macd")
   axis[0].plot(params._emaslow, 'r', label = "signal")
   #axis[0].plot(signal, 'r', label = "signal")
   #axis[1].plot(histogram, 'k', label = "histogram")
   #axis[1].plot(zeroLine, 'k')
   #axis[1].plot(derivative)
   #axis[1].legend()
   axis[1].set_xlim(range)

   plt.show()

   

   


if __name__ == "__main__":
   main()