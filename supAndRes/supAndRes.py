import numpy as np
import matplotlib.pyplot as plt
import time
from HIST_Manager import *

PATH_DATA = "D:\script\schei2\supAndRes\EUR_USD Dati Storici.csv"
#PATH_DATA = "D:\script\ptr\EUR_USD Dati Storici 2022.csv"
#PATH_DATA = "C:\Users\Marco\Documents\python\supAndRes\EUR_USD Dati Storici.csv"

MAX = 1
MIN = 2

class Point:
   def __init__(self, x, y):
      self.x = x
      self.y = y

#############################
#  private methods
#############################

def toDay(x):
   return x / (60 *24)

def toHour(x):
   return x / (60)

def LoadDataFromCSV():
   
   matrix = []

   f = open(PATH_DATA, 'r')
   lines = f.readlines()

   for i in range(len(lines)-1, 0, -1):   #leggi dati partendo dal fondo
      data = lines[i].split("\",\"")
      array = []
      n = data[1].replace('\'', '')
      array.append(float(data[1].replace('\'', '').replace(',','.')))
      array.append(float(data[2].replace('\'', '').replace(',','.')))
      array.append(float(data[3].replace('\'', '').replace(',','.')))
      array.append(float(data[4].replace('\'', '').replace(',','.')))
      matrix.append(array)

   matrix = np.array(matrix)

   return matrix

def DetectMax(x1, x2, x3):
   if(x1 < x2 and x3 < x2):
      return True
   else:
      return False
   
def DetectMin(x1, x2, x3):
   if(x2 < x1 and x2 < x3):
      return True
   else:
      return False
   
def AddValueToQueue(queue, value):
   queue.append(value)
   if(len(queue) == 4):
      queue.pop(0)

def DetectAllSequentPoints(whichPoints, data):
   dataLength = len(data)
   allPoint = []

   f = 0

   if(whichPoints == MAX):
      f = DetectMax
   elif(whichPoints == MIN):
      f = DetectMin

   start = 3
   stop = dataLength
   step = 1

   for i in range(start, stop, step):
      if(f(data[i-2], data[i-1], data[i]) == True):
         allPoint.append(Point(i-1, data[i-1]))

   return allPoint

def DetectAllSecondOrderPoints(whichPoints, points):
   AllSecondOrderMax = []

   f = 0

   if(whichPoints == MAX):
      f = DetectMax
   elif(whichPoints == MIN):
      f = DetectMin

   start = 3
   stop = len(points)
   step = 1

   for i in range(start, stop, step):
      first = points[i-2].y
      second = points[i-1].y
      third = points[i].y

      if(f(first, second, third) == True):
         AllSecondOrderMax.append(Point(points[i-1].x, second))

   return AllSecondOrderMax

def printLineFromFirstPointToThirdWithSlopeDueToSecondPoint(first, second, third, style):
   
   m = (first.y - second.y) / (first.x - second.x)
   q = first.y - m * first.x
   lastY = m * third.x + q
   fakePoint = Point(third.x, lastY)

   if(style == "dashed"):
      s = '--'
   elif(style == "dashdot"):
      s = '-.'
   elif(style == "dotted"):
      s = ':'

   x_values = [first.x, fakePoint.x]
   y_values = [first.y, fakePoint.y]
   #plt.plot(x_values, y_values, 'bo', linestyle="--")
   plt.plot(first.x, first.y, 'bo')
   plt.plot(second.x, second.y, 'bo')
   plt.plot(x_values, y_values, linestyle = s, color = 'k')

   return Point(second.x, m)
   
def printLineBetweenTwoPoints(first, second):
   x_values = [first.x, second.x]
   y_values = [first.y, second.y]
   plt.plot(x_values, y_values, 'bo', linestyle="--")

#############################
#  public methods
#############################

def originalMain():
   """
   funzione originale per plottare i valori massimi e minimi e una riga che collega tra di loro questi valori
   """
   
   lastThreeMax = []
   lastThreeMin = []
   
   data = LoadDataFromCSV()
   close = data[:, 0]

   #plt.plot(close)
   #plt.show()

   # to run GUI event loop
   plt.ion()
 
   # here we are creating sub plots
   figure, ax = plt.subplots()
   xRange = list(range(1, 30+1))
   yRange = np.linspace(min(close), max(close), 30)
   line1, line2, line3, = ax.plot(xRange, yRange)
   
   dataLength = len(close)

   start = 3
   stop = dataLength
   step = 1

   for i in range(start, stop, step):
      if(DetectMax(close[i-2], close[i-1], close[i]) == True):
         AddValueToQueue(lastThreeMax, Point(close[i-1], i-1))

      if(DetectMin(close[i-2], close[i-1], close[i]) == True):
         AddValueToQueue(lastThreeMin, Point(close[i-1], i-1))

      if(len(lastThreeMax) == 3):
         line2.set_xdata(list(range(1, 15)))
         line2.set_ydata(list(range(1, 15)))
      
      if(len(lastThreeMin) == 3):
         pass

      y = close[i:i+30]
      
      line1.set_xdata(xRange)
      line1.set_ydata(y)

      figure.canvas.draw()
      figure.canvas.flush_events()

      time.sleep(0.1)

def main():
   """
   anche questa trova minimi e massimi e plotta le linee che collegano questi tra di loro 
   """
   
   lastThreeMax = []
   lastThreeMin = []
   
   data = LoadDataFromCSV()
   close = data[:, 0]

   #plt.ion()
   plt.plot(close)
   #plt.show()

   AllMax = DetectAllSequentPoints(MAX, close)
   AllMin = DetectAllSequentPoints(MIN, close)
   secondOrderMax = DetectAllSecondOrderPoints(MAX, AllMax)
   secondOrderMin = DetectAllSecondOrderPoints(MIN, AllMin)
   slopeListMin = []
   slopeListMax = []
   
   for point in AllMax:
      x = point.x
      y = point.y
      #plt.plot(x, y, marker="o")
   
   for point in AllMin:
      x = point.x
      y = point.y
      #plt.plot(x, y, marker="x")
   
   for i in range(len(AllMin)-2):
      first = AllMin[i]
      second = AllMin[i+1]
      third = AllMin[i+2]
      m = printLineFromFirstPointToThirdWithSlopeDueToSecondPoint(first, second, third, "dashed")
      slopeListMin.append(m)

   for i in range(len(AllMin)-2):
      first = AllMax[i]
      second = AllMax[i+1]
      third = AllMax[i+2]
      m = printLineFromFirstPointToThirdWithSlopeDueToSecondPoint(first, second, third, "dotted")
      slopeListMax.append(m)

   plt.show()
   
   plt.figure()
   for i in range(len(slopeListMin)-1):
      printLineBetweenTwoPoints(slopeListMin[i], slopeListMin[i+1])
   for i in range(len(slopeListMax)-1):
      printLineBetweenTwoPoints(slopeListMax[i], slopeListMax[i+1])
   plt.show()

def testWithDataFromMinuteChart():
   """
   carica dei dati
   calcola massimi e minimi per ogni intervallo di tempo specificato nella funzione
   esegue plot di tutti massimi e minimi in una data sequenza temporle
   """
   
   data = load_HIST_Data()

   #close = np.array(data[:, 4])
   data = data[0:1000, :]
   close = np.array(data[:, 9])
   #close = close[0:24*60]
   
   #https://matplotlib.org/3.1.0/gallery/subplots_axes_and_figures/secondary_axis.html
   fig, ax = plt.subplots(constrained_layout=True)
   #secax = ax.secondary_xaxis('top', functions = (toDay, toDay))
   secax2 = ax.secondary_xaxis('top', functions = (toHour, toHour))

   ax.plot(close)

   hourData = HIST_findDataEveryTimeInterval(data, THIRTY_MINUTES)
   
   hourMin = HIST_findMinInPointSequence(hourData)
   hourMax = HIST_findMaxInPointSequence(hourData)
   
   #for i in range(len(hourMin)-1):
   #   printLineBetweenTwoPoints(hourMin[i], hourMin[i+1])
   #for i in range(len(hourMax)-1):
   #   printLineBetweenTwoPoints(hourMax[i], hourMax[i+1])
   
   for max in hourMax:
      plt.plot(max.x, max.y, 'bo')
   for min in hourMin:
      plt.plot(min.x, min.y, 'ro')


   plt.show()

def testPrintCertainNumberOfData():
   """
   esegue plot di dati con minimi e massimi in real time
   """
   
   allData = load_HIST_Data()
   allClose = np.array(allData[:, 9])
   
   currentData = []
   currentClose = []

   plt.ion()
   plt.show()
   counter = 0

   for i in range(len(allClose)):
      counter += int(1)
      currentData.append( allData[i] )
      currentClose.append( allClose[i] )
      #currentData = allData[i:i+100]
      #currentClose = allClose[i:i+100]

      if(len(currentData) > 200):
         currentData.pop(0)
         currentClose.pop(0)
         
      dataSampled = HIST_findDataEveryTimeInterval(currentData, FIVE_MINUTES)
      dataMin = HIST_findMinInPointSequence(dataSampled)
      dataMax = HIST_findMaxInPointSequence(dataSampled)
      
      lastTwoMax = []
      lastTwoMin = []
      
      if(len(dataMax) >= 2 and len(dataMin) >= 2):
         lenMax = len(dataMax)
         lastTwoMax.append(dataMax[lenMax - 1])
         lastTwoMax.append(dataMax[lenMax - 2])

         lenMin = len(dataMin)
         lastTwoMin.append(dataMin[lenMin - 1])
         lastTwoMin.append(dataMin[lenMin - 2])
         
         printLineFromFirstPointToThirdWithSlopeDueToSecondPoint(lastTwoMax[1], lastTwoMax[0], Point(len(currentClose)-1, currentClose[len(currentClose)-1]), "dashed")
         printLineFromFirstPointToThirdWithSlopeDueToSecondPoint(lastTwoMin[1], lastTwoMin[0], Point(len(currentClose)-1, currentClose[len(currentClose)-1]), "dotted")

      plt.plot(currentClose, 'k')
      for h in dataSampled:
         plt.plot(h.x, h.y, 'x')
      for max in dataMax:
         plt.plot(max.x, max.y, 'bs')
      for min in dataMin:
        plt.plot(min.x, min.y, 'ko')
      
      plt.pause(0.5)
      plt.clf()   #pulisce l'immagine
      plt.draw()
      
   print("end")

def plotDifferenceWithPreviousTimestamp():
   allData = load_HIST_Data()
   allClose = np.array(allData[:, 9])

   delta = []

   for i in range(len(allClose)):
      delta.append(allClose[i] - allClose[i-1])

   plt.plot(delta)
   plt.show()

if __name__ == "__main__":
   originalMain()
   #main()
   #testWithDataFromMinuteChart()
   #testPrintCertainNumberOfData()
   #plotDifferenceWithPreviousTimestamp()
