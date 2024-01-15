import pandas as pd
from copy import deepcopy
from pylab import *
from commons import LoadMostRecentValues
from commons import LogData
from commons import SaveMostRecentValues
from commons import AnalyzeLog
from commons import AnalizeOrders
from commons import function
from commons import WriteLog
import dataFolder.dataFiles
import multiprocessing


'''
goal:
- high global gain
- keep open position opened for as few days as possible
- high win/lose ratio

'''


#NOTA: la lenta deve sempre essere fatta su più campioni rispetto la veloce!!
FAST_PARAMETER_MIN_VALUE = 1
FAST_PARAMETER_MAX_VALUE = 25
SLOW_PARAMETER_MIN_VALUE = 1
SLOW_PARAMETER_MAX_VALUE = 40
SIGNAL_PARAMETER_MIN_VALUE = 1
SIGNAL_PARAMETER_MAX_VALUE = 30
EMA_PARAMETER_MAX_VALUE = 500
   

def getNextParameters():
   fastParam, slowParam, signalParam, ema = LoadMostRecentValues(dataFolder.dataFiles.PATH_LAST_PARAMETERS)

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

   SaveMostRecentValues(dataFolder.dataFiles.PATH_LAST_PARAMETERS, fastParam, slowParam, signalParam, ema)

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



def functionToCallInProcess(mutex, name):
   mutex["mutexLoadData"].acquire()
   data = pd.read_csv(dataFolder.dataFiles.BASE_PATH + dataFolder.dataFiles.FILE_2022_1M_WITH_CLASS)
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
   withProcesses()
   