#import yfinance as yf
import numpy as np
#import tensorflow
import matplotlib.pyplot as plt
import pandas_ta as ta
import pandas as pd
import math
import copy
from copy import deepcopy
from pathlib import Path
import os
from ta.trend import MACD
from ta.trend import EMAIndicator
from ta.volatility import BollingerBands
from pylab import *
from commons import Order
from commons import GetValueFromLines
from commons import LoadMostRecentValues
from commons import LogData
from commons import SaveMostRecentValues
from commons import AnalyzeLog
from commons import Status
from commons import AnalizeOrders
import multiprocessing
import plotVariPerCapireMeglioIDati
import dataFolder.dataFiles

'''
goal:
- high global gain
- keep open position opened for as few days as possible
- high win/lose ratio

'''


BASE_PATH = "daUSB/schei/EURUSD/"
PATH_LOG = "log.txt"
PATH_LAST_PARAMETERS = "last_parameters_macd.txt"
PATH_TEST_LAST_PARAMETERS = "test_last_parameters.txt"

#NOTA: la lenta deve sempre essere fatta su più campioni rispetto la veloce!!
FAST_PARAMETER_MIN_VALUE = 1
FAST_PARAMETER_MAX_VALUE = 25
SLOW_PARAMETER_MIN_VALUE = 1
SLOW_PARAMETER_MAX_VALUE = 40
SIGNAL_PARAMETER_MIN_VALUE = 1
SIGNAL_PARAMETER_MAX_VALUE = 30
EMA_PARAMETER_MAX_VALUE = 500
   

#############################
#  private methods
#############################

def WriteLog(logData):
   line = "{0},{1},{2},{3},{4},{5},{6},{7},{8}\n".format(logData.fastParam,
                                                logData.slowParam, 
                                                logData.signalParam, 
                                                logData.ema,
                                                logData.openDays, 
                                                logData.globalGain, 
                                                logData.goodTrades, 
                                                logData.badTrades,
                                                logData.numberOfBuySignals)
   f = open(BASE_PATH + PATH_LOG, "a")
   f.write(line)
   f.close()

def ComputeMACD(data, fast, slow, signal):
   #df = pd.DataFrame(data, columns = ['a'])
   #porcodio = ta.macd(data.iloc[:,1], fast = fast, slow = slow, signal = signal)
   #porcodio = np.array(porcodio)
   
   #usa questo se non parti da 0
   #df = pd.DataFrame(data, columns = ['a'])
   #porcodio = MACD(close = df.loc[:, 'a'], window_fast = fast, window_slow = slow, window_sign = signal)
   
   porcodio = MACD(close = data, window_fast = fast, window_slow = slow, window_sign = signal)
   macd = porcodio.macd()
   histogram = porcodio.macd_diff()
   sign = porcodio.macd_signal()
   
   return macd, histogram, sign

def order_openOrder(order, openPrice, openAt, orderType):
   order.openPrice = openPrice
   order.openAt = openAt
   order.operationType = orderType
   return order

def function(close, fastParam, slowParam, signalParam, ema):
   macd, histogram, signal = ComputeMACD(close, fastParam, slowParam, signalParam)
   macd = np.array(macd)
   histogram = np.array(histogram)
   signal = np.array(signal)
   length = close.shape[0]

   emaSignal = EMAIndicator(close = close, window = ema)
   emaSignal = emaSignal.ema_indicator()
   emaSignal = np.array(emaSignal)

   order = Order()
   status = Status()
   orders = []

   for i in range(0, length-1):
      if(math.isnan(macd[i]) == False and math.isnan(signal[i]) == False and math.isnan(emaSignal[i]) == False):
         status.UpdateStatus(macd[i], signal[i], histogram[i], emaSignal[i], close[i])

         buySignal = status.GenerateBuySignal()
         sellSignal = status.GenerateSellSignal()

         if(buySignal == True):
            status.numberOfBuySignals += int(1)
         
         if(sellSignal == True):
            status.numberOfSellSignals += int(1)
         
         if(status.currentlyHaveAnOrder == False):
            if(buySignal == True):
               status.currentlyHaveAnOrder = True
               order = order_openOrder(order, close[i], i, 'buy')                           
            elif(sellSignal == True):
               status.currentlyHaveAnOrder = True
               order = order_openOrder(order, close[i], i, 'sell')
         else:
            closeOrder = False

            if(order.operationType == 'buy'):
               #if(sellSignal == True):
               if(close[i] > order.openPrice + 0.001 or close[i] < order.openPrice - 0.001):
               #if(close[i] > order.openPrice + 0.01 or close[i] < order.openPrice - closeAt):
                  closeOrder = True
            elif(order.operationType == 'sell'):
               if(close[i] > order.openPrice + 0.001 or close[i] < order.openPrice - 0.001):
                  closeOrder = True

            if(closeOrder == True):
               order.closePrice = close[i]
               status.currentlyHaveAnOrder = False
               order.closeAt = i
               orders.append(deepcopy(order))
               order.Reset()
         
         status.UpdateAtTheEnd()
   
   return orders, status


#############################
#  public methods
#############################

def createLog():
   #data = LoadDataFromCSV(BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_window_100.csv")
   data = pd.read_csv(BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_window_100.csv")
   
   close = data.iloc[:,1]
   #close = data[0:1440]
   #close = np.array(close)   
   
   needToLoadMostRecentValues = True

   fastParam = FAST_PARAMETER_MIN_VALUE
   slowParam = SLOW_PARAMETER_MIN_VALUE
   signalParam = SIGNAL_PARAMETER_MIN_VALUE
   minPositiveGain = 0
   mostRecentefastParam, mostRecenteslowParam, mostRecentesignalParam, mostRecentMinPositiveGain = LoadMostRecentValues(BASE_PATH + PATH_LAST_PARAMETERS)
   
   while(fastParam < FAST_PARAMETER_MAX_VALUE):
      slowParam = fastParam + 1
      while(slowParam < SLOW_PARAMETER_MAX_VALUE):
         signalParam = SIGNAL_PARAMETER_MIN_VALUE
         while(signalParam < SIGNAL_PARAMETER_MAX_VALUE):

            if(needToLoadMostRecentValues == True):
               needToLoadMostRecentValues = False
               fastParam = mostRecentefastParam
               slowParam = mostRecenteslowParam
               signalParam = mostRecentesignalParam
            
            orders, status = function(close, fastParam, slowParam, signalParam)

            openDays, globalGain, goodTrades, badTrades = AnalizeOrders(orders)

            logData = LogData()
            logData.openDays = openDays
            logData.globalGain = "{:.6f}".format(round(globalGain, 6))
            logData.goodTrades = goodTrades
            logData.badTrades = badTrades
            logData.fastParam = fastParam
            logData.slowParam = slowParam
            logData.signalParam = signalParam
            #logData.closeAt = closeAt
            logData.numberOfBuySignals = status.numberOfBuySignals

            if(globalGain > 0):
               WriteLog(logData)

            SaveMostRecentValues(BASE_PATH + PATH_LAST_PARAMETERS, fastParam, slowParam, signalParam, 0)

            signalParam += int(1)
         slowParam += int(1)
      fastParam += int(1)

def plotin3d():
   f = open(BASE_PATH + PATH_LOG, "r")
   lines = f.readlines()

   globalGain = [] 
   
   for line in lines:
      data = line.split(',')
      #globalGain.append(float(data[4]))
      globalGain.append(float(data[5]))

   fast = GetValueFromLines(lines, 0)
   slow = GetValueFromLines(lines, 1)
   signal = GetValueFromLines(lines, 2)
   globalGain = np.array(globalGain)

   print(np.argmax(globalGain))

   localFast = []
   localSlow = []
   localSignal = []
   localGlobalGain = []

   for i in range(len(globalGain)):
      if(globalGain[i] > 0.04):
         localFast.append(fast[i])
         localSlow.append(slow[i])
         localSignal.append(signal[i])
         localGlobalGain.append(globalGain[i])

   fast = np.array(localFast)
   slow = np.array(localSlow)
   signal = np.array(localSignal)
   globalGain = np.array(localGlobalGain)
   
   # creating figures
   fig = plt.figure(figsize=(10, 10))
   ax = fig.add_subplot(111, projection='3d')
   
   # setting color bar
   color_map = cm.ScalarMappable(cmap=cm.Greens_r)
   color_map.set_array(globalGain)

   # creating the heatmap
   img = ax.scatter(fast, slow, signal, marker='o', color='green')
   plt.colorbar(color_map)

   # adding title and labels
   ax.set_title("3D Heatmap")
   ax.set_xlabel('fast')
   ax.set_ylabel('slow')
   ax.set_zlabel('signal')

   plt.show()

   a = 1

def writeGainForEachMonth():
   data = pd.read_csv(BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_window_100.csv")
   
   close = data.iloc[:,1]
   timestamp = data.iloc[:,0]
   
   MINUTES_IN_AN_HOUR = int(60)
   HOURS_IN_A_DAY = int(24)
   DAYS_IN_A_MONTH = int(21)
   minutesInAMonth = MINUTES_IN_AN_HOUR * HOURS_IN_A_DAY * DAYS_IN_A_MONTH
   minutesInaDay = MINUTES_IN_AN_HOUR * HOURS_IN_A_DAY
   
   for j in range(12):
      #fastParam = 12
      #slowParam = 26
      #signalParam = 9
      fastParam = 1
      slowParam = 2
      signalParam = 5

      data = timestamp
      data = data.to_numpy()
      data = data.tolist()
      for i in range(len(data)):
         data[i] = data[i].split(' ')[0]

      localClose = close.iloc[minutesInAMonth * j : minutesInAMonth * (j+1)]
      localClose = close
      localClose = np.array(localClose)   #usa questo se non parti da 0

      macd, histogram, signal = ComputeMACD(localClose, fastParam, slowParam, signalParam)
      macd = np.array(macd)
      histogram = np.array(histogram)
      signal = np.array(signal)
      
      order = Order()
      status = Status()
      orders = []
      tot = 0

      for i in range(0, len(localClose)-1):
         if(math.isnan(macd[i]) == False and math.isnan(signal[i]) == False):
            status.UpdateStatus(macd[i], signal[i], histogram[i])

            buySignal = status.GenerateBuySignal()
            sellSignal = status.GenerateSellSignal()

            if(buySignal == True):
               status.numberOfBuySignals += int(1)
            
            if(sellSignal == True):
               status.numberOfSellSignals += int(1)
            
            if(status.currentlyHaveAnOrder == False):
               if(buySignal == True):
                  status.currentlyHaveAnOrder = True
                  order = order_openOrder(order, close[i], i, 'buy')                           
               elif(sellSignal == True):
                  status.currentlyHaveAnOrder = True
                  order = order_openOrder(order, close[i], i, 'sell')
            else:
               closeOrder = False

               if(order.operationType == 'buy'):
                  #if(sellSignal == True):
                  if(close[i] > order.openPrice + 0.001 or close[i] < order.openPrice - 0.001):
                  #if(close[i] > order.openPrice + 0.01 or close[i] < order.openPrice - closeAt):
                     closeOrder = True
               elif(order.operationType == 'sell'):
                  if(close[i] > order.openPrice + 0.001 or close[i] < order.openPrice - 0.001):
                     closeOrder = True

               if(closeOrder == True):
                  order.closePrice = close[i]
                  status.currentlyHaveAnOrder = False
                  order.closeAt = i
                  orders.append(deepcopy(order))
                  order.Reset()

            status.UpdateAtTheEnd()

      openDays, globalGain, goodTrades, badTrades = AnalizeOrders(orders)
      tot = tot + globalGain

      gain = "{:.6f}".format(globalGain)
      print("{0}: {1}".format(str(j), str(gain)))
   print("tot = {:.6f}".format(tot))



def printDataAccordingToSelection():
   data = pd.read_csv(BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_gennaio_class.csv")
   
   close = data.iloc[:,3]
   state = data.iloc[:,6]

   MINUTES_IN_A_DAY = int(60 * 24)
   WHICH_DAY = int(0)
   start = MINUTES_IN_A_DAY * WHICH_DAY
   end = MINUTES_IN_A_DAY * (WHICH_DAY + 5)
   start = 413 + start
   end = 413 + end

   close = close[start:end]
   state = state[start:end]

   fast = 5
   slow = 10
   window = 7

   macd = MACD(close = close, window_slow = slow, window_fast = fast, window_sign = window)
   ema200 = EMAIndicator(close = close, window = 200)
   indicator_bb = BollingerBands(close = close, window = 200, window_dev = 2)
   bb_bbm = indicator_bb.bollinger_mavg()
   bb_bbh = indicator_bb.bollinger_hband()
   bb_bbl = indicator_bb.bollinger_lband()

   hist = macd.macd_diff()
   signal = macd.macd_signal()
   ema200 = ema200.ema_indicator()

   close = np.array(close)
   state = np.array(state)
   ema200 = np.array(ema200)
   bb_bbm = np.array(bb_bbm)
   bb_bbh = np.array(bb_bbh)
   bb_bbl = np.array(bb_bbl)

   #figure, axis = plt.subplots(2, 1)

   #axis[0].plot(close, color = 'b')
   #axis[0].plot(ema200, color = 'k')
   #axis[1].plot(hist, color = 'k', linestyle = 'dotted')
   #axis[1].plot(signal, color = 'k', linestyle = 'dashed')
   #for i in range(len(state)):
   #    if(state[i] == 1):
   #        axis[0].plot(i, close[i], marker = 'o', color = 'b')

   #plt.plot(close, color = 'b')
   #plt.plot(ema200, color = 'k', linestyle = 'dotted')
   #plt.plot(bb_bbm, color = 'k', linestyle = 'dashed')
   #plt.plot(bb_bbh, color = 'k', linestyle = 'dashed')
   #plt.plot(bb_bbl, color = 'k', linestyle = 'dashed')

   figure, axis = plt.subplots(2, 1)
   axis[0].plot(close, color = 'b')
   #plt.plot(bb_bbm, color = 'k', linestyle = 'dashed')
   axis[0].plot(bb_bbh, color = 'k', linestyle = 'dashed')
   axis[0].plot(bb_bbl, color = 'k', linestyle = 'dashed')
   average = np.array(indicator_bb._mavg)
   standardDeviation = np.array(indicator_bb._mstd)
   axis[1].plot(standardDeviation, color = 'r', linestyle = 'dashed')
   axis[1].plot(standardDeviation / average, color  = 'k', linestyle = 'dashed')
   
   #plt.xlim([0, 1500])
   axis[0].set_xlim([-10, MINUTES_IN_A_DAY * 5])
   axis[1].set_xlim([-10, MINUTES_IN_A_DAY * 5])
   plt.show()
      
      
def getNextParameters():
   fastParam, slowParam, signalParam, ema = LoadMostRecentValues(BASE_PATH + PATH_LAST_PARAMETERS)

   terminate = False

   if(fastParam == FAST_PARAMETER_MAX_VALUE and
      slowParam == SLOW_PARAMETER_MAX_VALUE and
      signalParam == SIGNAL_PARAMETER_MAX_VALUE and
      ema == EMA_PARAMETER_MAX_VALUE):
      terminate = True

   if(ema < EMA_PARAMETER_MAX_VALUE):
      ema += int(1)
   elif(signalParam < SIGNAL_PARAMETER_MAX_VALUE):
      ema = 1
      signalParam += int(1)
   elif(slowParam < SLOW_PARAMETER_MAX_VALUE):
      ema = 1
      slowParam += int(1)
      signalParam = SIGNAL_PARAMETER_MIN_VALUE
   elif(fastParam < FAST_PARAMETER_MAX_VALUE):
      ema = 1
      fastParam += int(1)
      slowParam = fastParam + 1
      signalParam = SIGNAL_PARAMETER_MIN_VALUE

   SaveMostRecentValues(BASE_PATH + PATH_LAST_PARAMETERS, fastParam, slowParam, signalParam, ema)

   values = {
      "slow": slowParam,
      "fast": fastParam,
      "signal": signalParam,
      "ema": ema,
      "terminate": terminate
   }

   return values

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
      p = multiprocessing.Process(target = functionToCallInProcess, args = (mutex, name))
      processList.append(p)
      processList[i].start()

   for i in range(numberOfCores):
      processList[i].join()

   '''
   p1 = multiprocessing.Process(target = functionToCallInProcess, args = (mutex, "p1"))
   p2 = multiprocessing.Process(target = functionToCallInProcess, args = (mutex, "p2"))
   p3 = multiprocessing.Process(target = functionToCallInProcess, args = (mutex, "p2"))
   p4 = multiprocessing.Process(target = functionToCallInProcess, args = (mutex, "p2"))
   p5 = multiprocessing.Process(target = functionToCallInProcess, args = (mutex, "p2"))
   p6 = multiprocessing.Process(target = functionToCallInProcess, args = (mutex, "p2"))
   
   p1.start()
   p2.start()
   p3.start()
   p4.start()
   p5.start()
   p6.start()

   p1.join()
   p2.join()
   p3.join()
   p4.join()
   p5.join()
   p6.join()
   '''

def functionToCallInProcess(mutex, name):
   mutex["mutexLoadData"].acquire()
   #data = pd.read_csv(BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_window_100.csv")
   data = pd.read_csv(BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_gennaio_class.csv")
   close = data.iloc[:,1]
   mutex["mutexLoadData"].release()
   
   keepGoing = True

   while(keepGoing):
      
      mutex["mutexLoadParameters"].acquire()
      #print(name + " lock")
      parameters = getNextParameters()
      #print(name + " unlock")
      mutex["mutexLoadParameters"].release()

      keepGoing = not parameters["terminate"]
      if(keepGoing):
         fast = parameters["fast"]
         slow = parameters["slow"]
         signal = parameters["signal"]
         ema = parameters["ema"]
         orders, status = function(close, fast, slow, signal, ema)
         openDays, globalGain, goodTrades, badTrades = AnalizeOrders(orders)

         logData = LogData()
         logData.openDays = openDays
         logData.globalGain = "{:.6f}".format(round(globalGain, 6))
         logData.goodTrades = goodTrades
         logData.badTrades = badTrades
         logData.fastParam = fast
         logData.slowParam = slow
         logData.signalParam = signal
         logData.ema = ema
         #logData.closeAt = closeAt
         logData.numberOfBuySignals = status.numberOfBuySignals

         if(globalGain > 0):
            mutex["mutexWriteResults"].acquire()
            WriteLog(logData)
            mutex["mutexWriteResults"].release()



if __name__ == "__main__":
   #createLog()
   #AnalyzeLog(BASE_PATH + PATH_LOG)
   #plotin3d()
   #writeGainForEachMonth()
   #printDataAccordingToSelection()

   #withProcesses()
   #plotOpenDaysHist()
   #plotGoodTradeRatioHist()
   #plotDeltaWithNextData(100)
   #plotNumberOfConsecutiveSecquences(POSITIVE_SEQUENCE)
   
   #plotAverageDifferenceInADay()

   #plotVariPerCapireMeglioIDati.plotTimeRequiredToGetACertainDifferenceInPosition(dataFolder.dataFiles.BASE_PATH + dataFolder.dataFiles.FILE_2022_1M_WITH_CLASS, 0.001)   
   #plotVariPerCapireMeglioIDati.plotNumberOfSignalsWhenChangingParameters(BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_gennaio_class.csv")
   #plotVariPerCapireMeglioIDati.plotDeltaWithNextData(5, dataFolder.dataFiles.FILE_FULL_PATH)
   plotVariPerCapireMeglioIDati.plotNumberOfConsecutiveSecquences(dataFolder.dataFiles.BASE_PATH + dataFolder.dataFiles.FILE_2022_1M_WITH_CLASS, 1)   
 