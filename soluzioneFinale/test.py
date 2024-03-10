

from ta.trend import MACD
from ta.trend import EMAIndicator
from ta.trend import SMAIndicator
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import multiprocessing
import random

import configuration
from manager import Manager
import order

def prRed(skk): print("\033[91m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[93m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))

def greatestFunctionEver():
   configuration.config.configurationUsed = configuration.DOUBLE_EMA
   filePath = "D:\script\schei2\supAndRes\DAT_ASCII_EURUSD_T_2022_onlyFebruary.csv"
   f = pd.read_csv(filePath)
   close = f.iloc[:,1]
   #close = close[0 : 120000]
   
   doAllTheWork = Manager(f, configuration.config)
   doAllTheWork.scanData()

   plt.plot(close, 'g')
   plt.plot(doAllTheWork.signals['slow'], '-b')
   plt.plot(doAllTheWork.signals['fast'], '-k')
   #plt.plot(doAllTheWork.signals['fast'] - doAllTheWork.signals['slow'], '-k')

   for o in doAllTheWork.orders:
      plt.plot(o.openedAtTime, o.openValue, 'o', color = 'b')
      plt.plot(o.closedAtTime, o.closeValue, 'o', color = 'k')

   tot = 0
   for o in doAllTheWork.orders:
      if(o.positionType == order.BUY):
         tot += o.closeValue - o.openValue
      if(o.positionType == order.SELL):
         tot += o.openValue - o.closeValue   
   tot = round(tot, 6)

   #plt.show()

   print('tot = ' + str(tot))
   #print(doAllTheWork.orders)
   
   for o in doAllTheWork.orders:
      if(o.positionType == order.BUY):
         result = o.closeValue - o.openValue
         if(result > 0):
            prGreen('b ' + str(round(result,6)))
         else:
            prRed('b ' + str(round(result,6)))

      if(o.positionType == order.SELL):
         result = o.closeValue - o.openValue   
         if(result < 0):
            prGreen('s ' + str(round(result,6)))
         else:
            prRed('s ' + str(round(result,6)))
   

def functionToBeCalledInProcess(name, mutex):
   print(name + " start")

   while(True):
      mutex["mutexLoadParameters"].acquire()
      filePath = "D:\script\schei2\supAndRes\DAT_ASCII_EURUSD_T_2022_onlyFebruary.csv"
      f = pd.read_csv(filePath)
      #close = f.iloc[:,1]

      localConfig = configuration.Configuration()
      
      localConfig.fastWindow = int(random.randrange(10, 50000, 10))
      localConfig.slowWindow = int(random.randrange(10, 100000, 10))
      localConfig.takeProfit = int(random.randrange(1, 100, 1))

      localConfig.stopLoss = int(random.randrange(1, int(localConfig.takeProfit * 1.2) + 1, 1) / 1000)

      localConfig.takeProfit = int(localConfig.takeProfit / 1000)
      
      localConfig.stopBy = configuration.FIXED_LIMTIS
      mutex["mutexLoadParameters"].release()
      
      doAllTheWork = Manager(f, localConfig)
      doAllTheWork.scanData()

      tot = 0
      for o in doAllTheWork.orders:
         if(o.positionType == order.BUY):
            tot += o.closeValue - o.openValue
         if(o.positionType == order.SELL):
            tot += o.openValue - o.closeValue   
      tot = round(tot, 6)

      if(tot > 0):
         print("{0},{1},{2},{3},{4},{5}".format(tot, localConfig.fastWindow, localConfig.slowWindow, localConfig.takeProfit, localConfig.stopLoss, len(doAllTheWork.orders) ))


def withProcesses():
   numberOfCores = multiprocessing.cpu_count() - int(3)

   mutex = {
      "mutexLoadParameters": multiprocessing.Lock(),
      "mutexLoadData": multiprocessing.Lock(),
      "mutexWriteResults": multiprocessing.Lock(),
   }

   processList = []
   for i in range(numberOfCores):
      name = 'p' + str(i)
      p = multiprocessing.Process(target = functionToBeCalledInProcess, args = (name, mutex))
      processList.append(p)
      processList[i].start()

   for i in range(numberOfCores):
      processList[i].join()

def main():
   #greatestFunctionEver()
   withProcesses()

from datetime import date

if __name__ == "__main__":
   main()

   print(date(year = 2024, month = 3, day = 4).weekday())
   print(date(year = 2024, month = 3, day = 5).weekday())
   print(date(year = 2024, month = 3, day = 6).weekday())
   print(date(year = 2024, month = 3, day = 7).weekday())
   print(date(year = 2024, month = 3, day = 8).weekday())
   print(date(year = 2024, month = 3, day = 9).weekday())
   print(date(year = 2024, month = 3, day = 10).weekday())