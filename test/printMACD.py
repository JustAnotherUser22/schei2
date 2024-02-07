
from ta.trend import MACD
import pandas as pd
import matplotlib.pyplot as plt


def main():
   filePath = "D:\script\schei2\supAndRes\DAT_ASCII_EURUSD_T_2022_onlyFebruary.csv"
   f = pd.read_csv(filePath)
   close = f.iloc[:,1]
   close = close[1:100]

   params = MACD(close = close, window_slow=26, window_fast=12, window_sign=9)
   macd = params.macd()
   signal = params.macd_signal()
   histogram = params.macd_diff()
   zeroLine = [0] * len(close)

   figure, axis = plt.subplots(2) 

   range = [-10, 110]

   axis[0].plot(close, label = "close")
   axis[0].legend()
   axis[0].set_xlim(range)


   axis[1].plot(macd, 'b', label = "macd")
   axis[1].plot(signal, 'r', label = "signal")
   axis[1].plot(histogram, 'k', label = "histogram")
   axis[1].plot(zeroLine, 'k')
   axis[1].legend()
   axis[1].set_xlim(range)

   plt.show()

   


if __name__ == "__main__":
   main()