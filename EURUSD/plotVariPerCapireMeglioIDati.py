
import matplotlib.pyplot as plt
import matplotlib


def getDataFromLine(line, positionToTake, separator):
   data = line.split(separator)
   toReturn = float(data[positionToTake])
   return toReturn


   
def plotDeltaWithNextData(distanceWithNexData, path):
   '''
   calcola da differenza tra ogni dato e il dato a "distanceWithNextData" entry di distanza
   da questo, poi mostra il tutto su un grafico
   '''
   #f = open(BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_formatted.csv", 'r')
   f = open(path)
   lines = f.readlines()
   lines = lines[1:] #rimuovo header
   
   allDelta = [] 
   
   for i in range(len(lines) - distanceWithNexData):
      currentData = getDataFromLine(lines[i], 2, ',')
      nextData = getDataFromLine(lines[i + distanceWithNexData], 2, ',')
      delta = nextData - currentData
      allDelta.append(delta)                                 

   matplotlib.pyplot.hist(allDelta, bins = 1000)
   matplotlib.pyplot.show() 

   plt.plot(allDelta)
   plt.show()


def plotAverageDifferenceInADay(path):
   '''
   in ogni giorno trova valore massimo e valore minimo e fa un plot 
   del delta tra i due (a cosa serve di preciso il tutto???)
   '''

   f = open(path, 'r')
   lines = f.readlines()
   lines = lines[1:] #rimuovo header
   length = len(lines)

   MINUTES_IN_A_DAY = int(60 * 24)
   start = MINUTES_IN_A_DAY * 0
   end = MINUTES_IN_A_DAY * 1
   start = 413 + start
   end = 413 + end

   deltas = []

   for start in range(413, length, MINUTES_IN_A_DAY):
      maxValue = getDataFromLine(lines[start], 2, ',')
      minValue = getDataFromLine(lines[start], 2, ',')

      lastValue = min(start + MINUTES_IN_A_DAY, length)
      for end in range(start + 1, lastValue, 1):
         currentData = getDataFromLine(lines[end], 2, ',')
         if(currentData > maxValue):
            maxValue = currentData
         if(currentData < minValue):
            minValue = currentData
      
      deltas.append(maxValue - minValue)
   
   matplotlib.pyplot.hist(deltas, bins = 100)
   matplotlib.pyplot.show() 

   plt.plot(deltas)
   plt.show()



def plotTimeRequiredToGetACertainDifferenceInPosition(filePath, differenceValue):
   '''
   per ogni valore che trova, conta tra quanto tempo troverò una differenza tra il valore
   attuale a un nuovo valore di almeno "differenceValue"
   '''
   
   f = open(filePath, 'r')
   lines = f.readlines()
   lines = lines[1:] #rimuovo header
   length = len(lines)

   totalCounters = []

   for i in range(0, length, 1):
      value = getDataFromLine(lines[i], 2, ',')
      contatore = 0

      for j in range(i + 1, length, 1):
         nextValue = getDataFromLine(lines[j], 2, ',')

         if(abs(nextValue - value) > differenceValue):
            totalCounters.append(contatore)
            break;
         else:
            contatore += int(1)

         #decido arbitrariamente di fermarmi dopo 3000 tentativi (valore totalmente a caso)
         if(contatore > 3000):
            break           

   matplotlib.pyplot.hist(totalCounters, bins = 1000)
   matplotlib.pyplot.show() 

   #plt.plot(totalCounters)
   #plt.show()


POSITIVE_SEQUENCE = 1
NEGATIVE_SEQUENCE = 2

def plotNumberOfConsecutiveSecquences(filePath, whichSequence):
   '''
   per ogni dato, conta per quante volte di seguito ci sarà un andamento crescente o decrescente del valore
   '''
   
   f = open(filePath, 'r')
   lines = f.readlines()
   lines = lines[1:] #rimuovo header

   #lines = lines[413 : 413+24*60]

   queue = []
   
   for i in range(1, len(lines)):
      currentLine = lines[i]
      data = currentLine.split(',')
      close = float(data[2])
      counter = 0
      currentMinOrMax = close

      for j in range(i+1, len(lines)):
         line = lines[j]
         nextData = line.split(',')
         nextClose = float(nextData[2])

         if(whichSequence == POSITIVE_SEQUENCE):
            condition = nextClose >= currentMinOrMax
         elif(whichSequence == NEGATIVE_SEQUENCE):
            condition = nextClose <= currentMinOrMax
   
         if(condition):
            counter += int(1)
            currentMinOrMax = nextClose
         else:
            break

      queue.append(counter)
      
   matplotlib.pyplot.hist(queue, bins = 200)
   matplotlib.pyplot.show() 

   plt.plot(queue)
   plt.show()

from ta.trend import EMAIndicator
from ta.trend import MACD
import numpy as np
import math
import pandas as pd
import matplotlib

def plotNumberOfSignalsWhenChangingParameters(filePath):
   data = pd.read_csv(filePath)   
   close = data.iloc[:,3]
   
   length = len(close)

   allCounters = []

   '''
   for w in range(2, 100):
      emaSignal = EMAIndicator(close = close, window = w)
      emaSignal = emaSignal.ema_indicator()
      emaSignal = np.array(emaSignal)
      contatore = 0

      for i in range(0, length, 1):
         
         if(math.isnan(emaSignal[i]) == False):
            value = close[i]
            currentEma = emaSignal[i]
            if(value > currentEma + 0.0015):
               contatore += int(1)
            if(value < currentEma - 0.0015):
               contatore += int(1)

      allCounters.append(contatore)

   plt.plot(allCounters)
   plt.show()
   '''

   fastArray = []
   slowArray = []
   signalArray = []

   for fast in range(2, 10):
      for slow in range(fast + 1, 20):
         for signal in range(1, 10):
            allMacd = MACD(close = close, window_fast = fast, window_slow = slow, window_sign = signal)
            macd = allMacd.macd()
            histogram = allMacd.macd_diff()
            sign = allMacd.macd_signal()
            macd = np.array(macd)
            histogram = np.array(histogram)
            sign = np.array(sign)
            contatore = 0

            for i in range(length):
               if(abs(macd[i] - sign[i]) < 0.00001):
                  contatore += int(1)
            
            fastArray.append(fast)
            slowArray.append(slow)
            signalArray.append(signal)
            allCounters.append(contatore)

   fastArray = np.array(fastArray)
   slowArray = np.array(slowArray)
   signalArray = np.array(signalArray)
   allCounters = np.array(allCounters)

   # creating figures
   fig = plt.figure(figsize=(10, 10))
   ax = fig.add_subplot(111, projection='3d')
   
   # setting color bar
   color_map = matplotlib.cm.ScalarMappable(cmap = matplotlib.cm.Greens_r)
   color_map.set_array(allCounters)

   # creating the heatmap
   img = ax.scatter(fastArray, slowArray, signalArray, marker='o', color='green')
   plt.colorbar(color_map)

   # adding title and labels
   ax.set_title("3D Heatmap")
   ax.set_xlabel('fast')
   ax.set_ylabel('slow')
   ax.set_zlabel('signal')
   plt.show()





