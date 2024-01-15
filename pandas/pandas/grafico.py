import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from ta.trend import EMAIndicator

BASE_PATH = "schei2/EURUSD/dataFolder/"
FILE_1M_ALL2022_WITH_CLASS = "DAT_ASCII_EURUSD_M1_2022_formatted_class.csv"
FILE_1M_ALL2022_ORIGNAL = "DAT_ASCII_EURUSD_M1_2022_formatted.csv"
FILE_1M_ALL2022_WINDOWS_100 = "DAT_ASCII_EURUSD_M1_2022_window_100.csv"
MINUTES_IN_A_DAY = int(60 * 24)

def plotDataAndMacdInMultiplePlot():

   data = pd.read_csv(BASE_PATH + FILE_1M_ALL2022_WINDOWS_100)
   (numberOfRows, numberOfColumns) = data.shape
   print("data set size = {0}".format(data.shape))

   close = data.iloc[:,3]
   state = data.iloc[:,6]
   
   start = MINUTES_IN_A_DAY * 0
   end = MINUTES_IN_A_DAY * 1
   start = 6140
   end = 6140+1440*2

   close = close[start:end]
   state = state[start:end]

   emafast = EMAIndicator(close = close, window = 60)
   emaslow = EMAIndicator(close = close, window = 100)
   emafast = np.array(emafast.ema_indicator())
   emaslow = np.array(emaslow.ema_indicator())
   signal = emafast - emaslow

   close = np.array(close)
   state = np.array(state)

   figure, axis = plt.subplots(2, 1)

   axis[0].plot(close, color = 'b')
   axis[0].plot(emafast, color = 'k', linestyle = 'dotted')
   axis[0].plot(emaslow, color = 'k', linestyle = 'dashed')
   #for i in range(len(state)):
   #    if(state[i] == 1):
   #        axis[0].plot(i, close[i], marker = 'o', color = 'b')

   axis[1].plot(signal)

   plt.show()



if __name__ == "__main__":
   plotDataAndMacdInMultiplePlot()
