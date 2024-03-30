

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
      #filePath = "D:\script\schei2\supAndRes\DAT_ASCII_EURUSD_T_2022_onlyFebruary.csv"
      filePath = "D:\script\schei2\EURUSD\dataFolder\DAT_ASCII_EURUSD_M1_2022_formatted.csv"
      f = pd.read_csv(filePath)
      #close = f.iloc[:,1]
      
      localConfig = configuration.Configuration()
      
      #la veloce deve essere su meno campioni della lenta (penso...)
      localConfig.fastWindow = int(random.randrange(10, 50000, 10))
      localConfig.slowWindow = int(random.randrange(localConfig.fastWindow, 100000, 10))
      localConfig.takeProfit = int(random.randrange(1, 100, 1))

      #localConfig.stopLoss = float(random.randrange(1, int(localConfig.takeProfit * 1.2) + 1, 1) / 10000)
      localConfig.stopLoss = float(random.randrange(1, 100, 1) / 10000)

      localConfig.takeProfit = float(localConfig.takeProfit / 10000)
      
      #localConfig.stopBy = configuration.FIXED_LIMTIS
      localConfig.stopBy = configuration.TRAILING_TAKE_PROFIT

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

      #if(tot > 0):
      #   print("{0},{1},{2},{3},{4},{5}".format(tot, localConfig.fastWindow, localConfig.slowWindow, localConfig.takeProfit, localConfig.stopLoss, len(doAllTheWork.orders) ))
      mutex["mutexWriteResults"].acquire()
      line = "{0},{1},{2},{3},{4},{5}".format(tot, localConfig.fastWindow, localConfig.slowWindow, localConfig.takeProfit, localConfig.stopLoss, len(doAllTheWork.orders))
      print(line)
      f = open("schei2/soluzioneFinale/results.txt", "a")
      f.write(line + '\n')
      f.close()
      mutex["mutexWriteResults"].release()


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


def showResultWithLessDimensions():
   from sklearn.decomposition import PCA

   X = pd.read_csv("schei2/soluzioneFinale/results.txt")
   print(X)

   from sklearn.preprocessing import StandardScaler
   X_std = StandardScaler().fit_transform(X.drop(columns=["tot"]))
   pca = PCA(n_components = 2) # vogliamo proiettare due dimensioni in modo da poterle visualizzare!
   
   # Addestriamo il modello PCA sui dati standardizzati
   vecs = pca.fit_transform(X_std)
   print(vecs)
   print(pca.singular_values_)
   print(pca.explained_variance_ratio_)
   
   '''   
   reduced_df = pd.DataFrame(data=vecs, columns=['Principal Component 1'])
   final_df = pd.concat([reduced_df, X[['tot']]], axis=1)
   plt.scatter(final_df["Principal Component 1"], final_df['tot'])
   plt.show()
   '''   
   
   reduced_df = pd.DataFrame(data=vecs, columns=['Principal Component 1', "Principal Component 2"])
   final_df = pd.concat([reduced_df, X[['tot']]], axis=1)
   fig = plt.figure()
   ax = plt.axes(projection='3d')
   
   # Data for a three-dimensional line
   zline = X['tot']
   xline = (reduced_df['Principal Component 1'])
   yline = (reduced_df['Principal Component 2'])
   #ax.plot3D(xline, yline, zline, 'gray')
   ax.scatter3D(xline, yline, zline, 'gray')
   plt.show()
   
   '''
   reduced_df = pd.DataFrame(data=vecs, columns=['Principal Component 1', "Principal Component 2", "pc3"])
   final_df = pd.concat([reduced_df, X[['tot']]], axis=1)
   fig = plt.figure()
   ax = plt.axes(projection='3d')

   final_df = final_df.where(final_df['tot'] > 0.08)
   
   # Data for a three-dimensional line
   c = final_df['tot']
   x = (final_df['Principal Component 1'])
   y = (final_df['Principal Component 2'])
   z = final_df['pc3']
   ax.set_xlabel('p1')
   ax.set_ylabel('p2')
   ax.set_zlabel('p3')
   img = ax.scatter(x, y, z, c=c, cmap=plt.hot())
   fig.colorbar(img)
   plt.show()
   '''
   
   print(pca.singular_values_)
   print(pca.components_)

   

def printUnaRoba():
   from ta.trend import EMAIndicator

   filePath = "D:\script\schei2\EURUSD\dataFolder\DAT_ASCII_EURUSD_M1_2022_formatted.csv"
   f = pd.read_csv(filePath)
   close = f.iloc[:, 1]

   ema = EMAIndicator(close = close, window = 20000)

   plt.plot(close)
   plt.plot(ema.ema_indicator())
   plt.show()




def main():
   #greatestFunctionEver()
   withProcesses()
   #showResultWithLessDimensions()
   #printUnaRoba()


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