from data import *
from algorithm import *
from broker import *
from messages import *
from manager import *
from history import *
from plotter import *
import matplotlib.pyplot as plt


'''
qui c'è il main vero e proprio
'''

PATH_LOG = "D:/script/events/log_ma_2022_feb_3to7.txt"
PATH_LAST_PARAMETERS = "D:/script/events/last_parameters.txt"


def dispatchFunction(message):
   dataReader.messageHandler(message)
   algorithm.messageHandler(message)
   manager.messageHandler(message)
   history.messageHandler(message)
   plotter.messageHandler(message)

def performSingleIteration():
   
   threshold = int(1)
   numberOfSamples = int(2)
   delta = float(0.0001)

   publishResetMessage()

   algorithm.localAlgo.NUMBER_OF_SAMPLES = int(numberOfSamples)
   algorithm.localAlgo.THRESHOLD = int(threshold)
   manager.PROFIT_OR_STOP_DELTA = float(delta)

   while(dataReader.dataEnded == False):
      dataReader.manager()
      algorithm.manager()
      manager.manager()
      history.manager()

   #history.printAll()
   history.printFinalGain()
   
   #average = [None] * algorithm.localAlgo.NUMBER_OF_SAMPLES
   #average.extend(plotter.macdData)
   plt.plot(plotter.allData)
   #plt.plot(average)
   for open in plotter.openPositions:
      plt.plot(open.x, open.y, 'bo')
   for close in plotter.closePositions:
      plt.plot(close.x, close.y, 'ro')
   plt.show()

   print("end")


def performMultipleIteration():
   needToLoadData = True
   lastNumber, lastThreashold, lastDelta = LoadMostRecentValues()

   threshold = int(1)
   numberOfSamples = int(2)
   delta = float(0.0001)

   while(threshold < 100):
      numberOfSamples = int(2)
      while(numberOfSamples < 200):
         delta = float(0.0001)
         while(delta < 0.0005):
            publishResetMessage()

            if(needToLoadData == True):
               needToLoadData = False
               threshold = lastThreashold
               numberOfSamples = lastNumber
               delta = lastDelta

            algorithm.localAlgo.NUMBER_OF_SAMPLES = int(numberOfSamples)
            algorithm.localAlgo.THRESHOLD = int(threshold)
            manager.PROFIT_OR_STOP_DELTA = float(delta)

            while(dataReader.dataEnded == False):
               dataReader.manager()
               algorithm.manager()
               manager.manager()
               history.manager()

            #history.printAll()
            history.printFinalGain()
            line = "{0},{1},{2}".format(numberOfSamples, threshold, delta)
            line += ','
            line += history.line + '\n'
            f = open(PATH_LOG, "a")
            f.write(line)
            f.close()

            SaveMostRecentValues(numberOfSamples, threshold, delta)
            delta += float(0.0001)
         numberOfSamples += int(1)
      threshold += int(1)
         

   average = [None] * algorithm.localAlgo.NUMBER_OF_SAMPLES
   average.extend(plotter.macdData)
   plt.plot(plotter.allData)
   #plt.plot(average)
   #for open in plotter.allOpen:
   #   plt.plot(open.x, open.y, 'bo')
   #for close in plotter.allClose:
   #   plt.plot(close.x, close.y, 'ro')
   plt.show()

   print("end")


def main():
   broker_setDispatchFunction(dispatchFunction)
   performSingleIteration()
   

def publishResetMessage():
   message = Message()
   message.header.sender = SENDER_APPLICATION
   message.header.type = RESET
   broker.dispatch(message)



def LoadMostRecentValues():
   f = open(PATH_LAST_PARAMETERS, 'r')
   lines = f.readlines()
   
   param1 = int(lines[0].replace('\n', ''))
   param2 = int(lines[1].replace('\n', ''))
   param3 = float(lines[2].replace('\n', ''))
   param3 = round(param3, 6)
   
   return (param1, param2, param3)

def SaveMostRecentValues(numberOfSamples, threshold, delta):
   f = open(PATH_LAST_PARAMETERS, 'w')
   f.write(str(numberOfSamples) + '\n')
   f.write(str(threshold) + '\n')   
   f.write(str(round(delta, 6)) + '\n')   

def plot3DplotAfterGenerateLog():
   fig = plt.figure()
   ax = plt.axes(projection = '3d')

   f = open(PATH_LOG, 'r')
   lines = f.readlines()
   
   zline = []
   xline = []
   yline = []
   all = []

   for line in lines:
      data = line.split(',')

      param1 = int(data[0])
      param2 = int(data[1])
      param3 = float(data[2])
      good = int(data[3])
      bad = int(data[4])
      ratio = float(data[5].replace('\n', ''))      

      xline.append(param1)
      yline.append(param2)
      zline.append(ratio)
      all.append([param1, param2, param3, good, bad, ratio])

   all = sorted(all, key = lambda tup: tup[5], reverse = True)

   ax.plot3D(xline, yline, zline, 'gray')
   plt.show()


if __name__ == "__main__":
   main()
   #plot3DplotAfterGenerateLog()