
from ta.volatility import BollingerBands
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def main():
   filePath = "D:\script\schei2\supAndRes\DAT_ASCII_EURUSD_T_2022_onlyFebruary.csv"
   f = pd.read_csv(filePath)
   close = f.iloc[:,1]
   #close = close[0:1000000]
   #close = close[1:100]
   #close = close[1:63897]  #1 giorno
   #close = close[63898 : 119401]  #secondo giorno
   close = close[0 : 119401]  #secondo giorno

   params = BollingerBands(close = close, window = 20000, window_dev = 1.5)
   h = params.bollinger_hband()
   l = params.bollinger_lband()
   c = params.bollinger_mavg()

   derivative = np.gradient(c, 1)
   derivative2 = np.gradient(derivative, 1)

   plt.plot(close, color = 'red')
   #plt.plot(h, color = 'black')
   #plt.plot(l, color = 'blue')
   plt.plot(c, color = 'green')
   
   #plt.plot(derivative2)

   plt.show()

   


if __name__ == "__main__":
   main()