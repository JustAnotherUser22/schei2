
from data import *
from algorithm import *
from broker import *
from messages import *
from manager import *
from history import *
from plotter import *
import matplotlib.pyplot as plt
import multiprocessing
import datetime


def mainWithProcess(name):
   
   start = datetime.datetime.now()
   print("{0} start at {1}".format(name, start))

   broker = Broker(BLOCKING)
   dataReader = DataReader(broker)
   algorithm = Algorithm(broker)
   manager = Manager(broker)
   history = History(broker)
   
   broker.subscribers.append(dataReader)
   broker.subscribers.append(algorithm)
   broker.subscribers.append(manager)
   broker.subscribers.append(history)
   
   while(dataReader.dataEnded == False):
      dataReader.manager()
      algorithm.manager()
      manager.manager()
      history.manager()

   #history.printAll()
   history.printFinalGain()

   delta = datetime.datetime.now() - start
   print("{0} end in {1}".format(name, delta))




def main():
   numberOfCores = 3#multiprocessing.cpu_count() - int(3)

   processList = []
   for i in range(numberOfCores):
      name = 'p' + str(i)
      p = multiprocessing.Process(target = mainWithProcess, args = (name, ))
      processList.append(p)
      processList[i].start()

   for i in range(numberOfCores):
      processList[i].join()



if __name__ == "__main__":
   main()
   #mainWithProcess('aaa')