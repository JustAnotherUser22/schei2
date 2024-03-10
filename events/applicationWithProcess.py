
from data import *
from algorithm import *
from broker import *
from messages import *
from manager import *
from history import *
import multiprocessing
import datetime
import random


#NOTA: la lenta deve sempre essere fatta su più campioni rispetto la veloce!!

FAST_PARAMETER_MIN_VALUE = 1
FAST_PARAMETER_MAX_VALUE = 200
FAST_PARAMETER_STEP = 10

SLOW_PARAMETER_MIN_VALUE = 1
SLOW_PARAMETER_MAX_VALUE = 400
SLOW_PARAMETER_STEP = 10

SIGNAL_PARAMETER_MIN_VALUE = 1
SIGNAL_PARAMETER_MAX_VALUE = 300
SIGNAL_PARAMETER_STEP = 10

PATH_PARAMETERS = 'schei2\events\parameters.txt'
PATH_LOG = 'schei2\events\log.txt'

def LoadMostRecentValues():
   f = open(PATH_PARAMETERS, 'r')
   lines = f.readlines()
   
   param1 = int(lines[0].replace('\n', ''))
   param2 = int(lines[1].replace('\n', ''))
   param3 = int(lines[2].replace('\n', ''))

   return (param1, param2, param3)

def SaveMostRecentValues(fast, slow, signal):
   f = open(PATH_PARAMETERS, 'w')
   f.write(str(fast) + '\n')
   f.write(str(slow) + '\n')
   f.write(str(signal) + '\n')
   f.close()

class Parameters():
   def __init__(self):
      self.fast = FAST_PARAMETER_MIN_VALUE
      self.slow = SLOW_PARAMETER_MIN_VALUE
      self.signal = SIGNAL_PARAMETER_MIN_VALUE


lastParameters = Parameters()

def getNextParameters():
   fastParam, slowParam, signalParam = LoadMostRecentValues()

   terminate = False

   if(fastParam >= FAST_PARAMETER_MAX_VALUE and
      slowParam >= SLOW_PARAMETER_MAX_VALUE and
      signalParam >= SIGNAL_PARAMETER_MAX_VALUE):
      terminate = True

   if(signalParam < SIGNAL_PARAMETER_MAX_VALUE):
      signalParam += SIGNAL_PARAMETER_STEP
   elif(slowParam < SLOW_PARAMETER_MAX_VALUE):
      slowParam += SLOW_PARAMETER_STEP
      signalParam = SIGNAL_PARAMETER_MIN_VALUE
   elif(fastParam < FAST_PARAMETER_MAX_VALUE):
      fastParam += FAST_PARAMETER_MAX_VALUE
      slowParam = fastParam + 1
      signalParam = SIGNAL_PARAMETER_MIN_VALUE

   lastParameters.fast = fastParam
   lastParameters.slow = slowParam
   lastParameters.signal = signalParam


   values = {
      "slow": slowParam,
      "fast": fastParam,
      "signal": signalParam,
      "terminate": terminate
   }

   SaveMostRecentValues(fastParam, slowParam, signalParam)

   return values

def GenerateRandomParameters():
   fastParam = random.uniform(1, 5)
   signalParam = random.uniform(0, 5)
   fastParam = int(10**fastParam)
   signalParam = int(10**signalParam)
   slowParam = 0

   while (slowParam < fastParam):
      slowParam = random.uniform(1, 6)
      slowParam = int(10**slowParam)

   values = {
      "slow": slowParam,
      "fast": fastParam,
      "signal": signalParam,
      "terminate": False
   }

   return values


def mainWithProcess(name, mutex):
   
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

   keepGoing = True
   
   while(keepGoing):

      mutex["mutexLoadParameters"].acquire()
      #parameters = getNextParameters()      
      parameters = GenerateRandomParameters()      
      mutex["mutexLoadParameters"].release()

      keepGoing = not parameters["terminate"]

      if(keepGoing):
         publishResetMessage(broker)
         algorithm.localAlgo.fast = parameters["fast"]
         algorithm.localAlgo.slow = parameters["slow"]
         algorithm.localAlgo.signal = parameters["signal"]
         while(dataReader.dataEnded == False):
            dataReader.manager()
            algorithm.manager()
            manager.manager()
            history.manager()
         history.printFinalGain()
         line = "{0}, {1}, {2}, {3}\n".format(parameters["fast"], parameters["slow"], parameters["signal"], history.line)
         
      mutex["mutexWriteResults"].acquire()
      f = open(PATH_LOG, 'a')
      f.write(line)
      f.close()
      mutex["mutexWriteResults"].release()

   print("end {0}".format(name))

   #delta = datetime.datetime.now() - start
   #print("{0} end in {1}".format(name, delta))


def publishResetMessage(broker):
   message = Message()
   message.header.sender = SENDER_APPLICATION
   message.header.type = RESET
   broker.dispatch(message)



def main():
   numberOfCores = 1#multiprocessing.cpu_count() - int(4)

   mutex = {
      "mutexLoadParameters": multiprocessing.Lock(),
      "mutexLoadData": multiprocessing.Lock(),
      "mutexWriteResults": multiprocessing.Lock(),
   }

   processList = []
   for i in range(numberOfCores):
      name = 'p' + str(i)
      p = multiprocessing.Process(target = mainWithProcess, args = (name, mutex))
      processList.append(p)
      processList[i].start()

   for i in range(numberOfCores):
      processList[i].join()



if __name__ == "__main__":
   main()

   mutex = {
      "mutexLoadParameters": multiprocessing.Lock(),
      "mutexLoadData": multiprocessing.Lock(),
      "mutexWriteResults": multiprocessing.Lock(),
   }
   #mainWithProcess('aaa', mutex)