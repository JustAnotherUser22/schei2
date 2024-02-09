
from ta.momentum import RSIIndicator
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
   filePath = "D:\script\schei2\supAndRes\DAT_ASCII_EURUSD_T_2022_onlyFebruary.csv"
   f = pd.read_csv(filePath)
   close = f.iloc[:,1]
   close = close[1:100]

   params = RSIIndicator(close = close, window = 20)
   rsi = params.rsi()

   diff = np.gradient(rsi)
   
   figure, axis = plt.subplots(2) 

   range = [-10, 110]

   axis[0].plot(close, label = "close")
   axis[0].legend()
   axis[0].set_xlim(range)


   axis[1].plot(rsi, 'b', label = "RSI")
   axis[1].plot(diff, 'k', label = "diff")
   axis[1].legend()
   axis[1].set_xlim(range)

   plt.show()

   


if __name__ == "__main__":
   main()