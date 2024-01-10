
import math
import numpy as np
import tensorflow as tf
from keras import models
from keras import layers
from deleteMe import fromNetworkToArray
from deleteMe import fromArrayToNetwork
from deleteMe import crossArray
import random
import matplotlib.pyplot as plt
import datetime

NUMBER_OF_POPULATION = 50
NUMBER_OF_MODEL = 100
WEIGHTS_DIRECTORY = "D:/script/GenAl/weights/"
LAST = NUMBER_OF_MODEL - 1

modelsList = []
results = []
populationList = []

class Entry:
   def __init__(self, network, result):
      self.network = network
      self.result = result

class Population:
   def __init__(self, dimension):
      self.dimension = dimension
      self.samples = []
      self.averageScore = 0
      self.ricombinationProbability = 100#30
      self.crossProbability = 10#2

   def initialize(self):
      for i in range(0, self.dimension):
         network = createCustomNetwork()
         tmpEntry = Entry(network, 0)
         self.samples.append(tmpEntry)

   def updateEveryEntry(self, test, test_output):
      for i in range(0, self.dimension):
         self.samples[i].result = abs(self.samples[i].network.predict(test, verbose = 0) - test_output)
         self.samples[i].result = self.computeResult(self.samples[i].result)

      self.samples.sort(key = lambda x: x.result, reverse = False)
      
   def updatePopulation(self, test, test_output):
      n1 = random.randint(0, self.dimension/2)
      n2 = random.randint(0, self.dimension/2)

      (w1, b) = fromNetworkToArray(self.samples[n1].network)
      (w2, b) = fromNetworkToArray(self.samples[n2].network)
      crossArray(w1, w2, self.ricombinationProbability, self.crossProbability)
      
      fromArrayToNetwork(self.samples[LAST].network, w1, b)

      self.samples[LAST].result = abs(self.samples[LAST].network.predict(test, verbose = 0) - test_output)
      self.samples[LAST].result = self.computeResult(self.samples[LAST].result)

      self.samples.sort(key = lambda x: x.result, reverse = False)

   def computeAverageScore(self):
      
      total = 0

      for i in range(0, self.dimension):
         total += float(self.samples[i].result)

      self.averageScore = total / self.dimension

      bestScore = self.samples[0].result
      diff = self.averageScore - bestScore
      
      self.ricombinationProbability = diff / 10
      self.crossProbability = 100 / diff

   def computeResult(self, data):
      return data[0][0]**2 + data[0][1]**2 + data[0][2]**2

##############################
#  metodi privati
##############################

def createCustomNetwork():

   initializer = tf.keras.initializers.RandomUniform(minval = -2, maxval = 2, seed = 0)

   network = models.Sequential()
   network.add(layers.Dense(2, activation='relu', input_shape=(2,), kernel_initializer = initializer, bias_initializer = initializer))
   #network.add(layers.Dense(1))
   
   #network.add(layers.Dense(2, kernel_initializer = initializer))
   #network.add(layers.Dense(2, kernel_initializer = initializer))
   #network.add(layers.Dense(2, kernel_initializer = initializer))

   #network.add(layers.Dense(2, kernel_initializer = initializer))  
   
   network.add(layers.Dense(1, kernel_initializer = initializer))
   return network

def plotResults(value):
   #value = [1,2,3,4,5,6,7,8,9,10]

   epochs = range(1, len(value) + 1)
   plt.clf()   #pulisce l'immagine, così plot successivi non si sovrappongono
   plt.plot(epochs, value, 'r', label='Training loss')
   #plt.title('andamento loss')
   #plt.xlabel('model number')
   #plt.ylabel('Loss')
   #plt.legend()
   #plt.ion()
   #plt.show()
   plt.draw()
   
   plt.pause(0.001)

##############################
#  metodi pubblici
##############################

def createModels():
   for i in range(0, NUMBER_OF_MODEL):
      network = createCustomNetwork()
      
      tmpEntry = Entry(network, 0)
      modelsList.append(tmpEntry)

def changeRandomValue(network):
   #https://stackoverflow.com/questions/44938160/saving-layer-weights-at-each-epoch-during-training-into-a-numpy-type-array-conv
   modelWeights = []
   for layer in network.layers:
      for weight in layer.get_weights():
         print(weight)
      
   array = []
   for w in modelWeights:
      array.append(w)

def computeResults(test, test_output):
   for i in range(0, NUMBER_OF_MODEL):
      modelsList[i].result = abs(modelsList[i].network.predict(test, verbose = 0) - test_output)
      modelsList[i].result = modelsList[i].result[0][0] + modelsList[i].result[0][1] + modelsList[i].result[0][2]

def findIndexOfMinimumValue():
   index = 0
   value = 0
   for i in range(0, NUMBER_OF_MODEL):
      if(results[i] < value):
         index = i
         value = results[i]
   return index

def updateModel(test, test_output):
   n1 = random.randint(0, NUMBER_OF_MODEL/2)
   n2 = random.randint(0, NUMBER_OF_MODEL/2)

   (w1, b) = fromNetworkToArray(modelsList[n1].network)
   (w2, b) = fromNetworkToArray(modelsList[n2].network)
   crossArray(w1, w2)
   
   fromArrayToNetwork(modelsList[LAST].network, w1, b)

   modelsList[LAST].result = abs(modelsList[LAST].network.predict(test, verbose = 0) - test_output)
   modelsList[LAST].result = modelsList[LAST].result[0][0] + modelsList[LAST].result[0][1] + modelsList[LAST].result[0][2]
   
   modelsList.sort(key = lambda x: x.result, reverse = False)


##############################
#  script
##############################

def single():
   createModels()

   #usati per non blocare lo script durante il plot del grafico
   plt.ion()
   plt.show()
   #plt.figure(figsize=(4, 2))

   test = np.array( [[15.21, 35.44], [18.45, 64.22], [84.13, 54.18]] )
   test_output = np.array( [50.65, 82.67, 138.31] )

   NUMERO_DI_CICLI = 100000
   WHEN_TO_PRINT = NUMERO_DI_CICLI

   computeResults(test, test_output)
   modelsList.sort(key = lambda x: x.result, reverse = False)

   for cycleNumber in range(0, NUMERO_DI_CICLI):
      
      line = str(datetime.datetime.now()) + ': '
      line += "iteration n = " + str(cycleNumber) + ', '
      line += "best = " + str(round(modelsList[0].result, 4)) + ', '
      line += "worst = " + str(round(modelsList[LAST].result, 4)) + ', '
      print(line)

      #for i in range(0, 10):
      #   print(modelsList[i].result)
      #print("-------------")

      updateModel(test, test_output)
      
      if(cycleNumber % WHEN_TO_PRINT == 0):
         value = []
         for i in range(0, NUMBER_OF_MODEL):
            value.append(float(modelsList[i].result))   
         #plotResults(value)
      
   print("END")

def multiple():
   
   #usati per non blocare lo script durante il plot del grafico
   plt.ion()
   plt.show()
   #plt.figure(figsize=(4, 2))

   test = np.array( [[15.21, 35.44], [18.45, 64.22], [84.13, 54.18]] )
   test_output = np.array( [50.65, 82.67, 138.31] )

   NUMERO_DI_CICLI = 100000
   WHEN_TO_PRINT = NUMERO_DI_CICLI
   WHEN_TO_SAVE = NUMERO_DI_CICLI

   for i in range(0, NUMBER_OF_POPULATION):
      tmp = Population(NUMBER_OF_MODEL)
      tmp.initialize()
      tmp.updateEveryEntry(test, test_output)
      populationList.append(tmp)
      print("population " + str(i) + " initialized")

   initialCycleNumber = LoadAllWeights()
   initialCycleNumber += 1
   #initialCycleNumber = 0

   for cycleNumber in range(initialCycleNumber, NUMERO_DI_CICLI):
      for i in range(0, NUMBER_OF_POPULATION):
         populationList[i].updatePopulation(test, test_output)
         
      if(cycleNumber % 10 == 0):
         for j in range(0, NUMBER_OF_POPULATION):
            #https://stackoverflow.com/questions/8234445/format-output-string-right-alignment
            #https://stackoverflow.com/questions/50756795/python-print-a-float-with-a-given-number-of-digits
            line = "population = {:>4}".format(j) + ', '
            line += "iteration n = {:>4}".format(cycleNumber) + ', '
            line += "best = {:07.3f}".format(round(populationList[j].samples[0].result, 4)) + ', '
            line += "worst = {:07.3f}".format(round(populationList[j].samples[LAST].result, 4)) + ', '
            print(line)

      if(cycleNumber % WHEN_TO_SAVE == 0 and cycleNumber != 0):
         SaveAllWeights(cycleNumber)

      var = 0
      if(var == 1):
         print(populationList[0].samples[0].network.get_weights())
         


   print("END")
      
   
def SaveAllWeights(numberToSave):
   checkpoint_path = "D:/script/GenAl/weights/"
   checkpoint_name = "population_{0}_entry_{1}"
   
   for j in range(0, NUMBER_OF_POPULATION):
      for k in range(0, NUMBER_OF_MODEL):
         populationList[j].samples[k].network.save_weights(checkpoint_path + checkpoint_name.format(j, k))

   currentIterationFile = "D:/script/GenAl/weights/currentIteration.txt"
   inputFile = open(currentIterationFile, "w")
   inputFile.write(str(numberToSave))

   


def LoadAllWeights():
   checkpoint_path = "D:/script/GenAl/weights/"
   checkpoint_name = "population_{0}_entry_{1}"
   
   for j in range(0, NUMBER_OF_POPULATION):
      for k in range(0, NUMBER_OF_MODEL):
         populationList[j].samples[k].network.load_weights(checkpoint_path + checkpoint_name.format(j, k))

   currentIterationFile = "D:/script/GenAl/weights/currentIteration.txt"
   inputFile = open(currentIterationFile)
   line = inputFile.readline()
   print("last iteration number = " + line)
   return int(line)



if __name__ == "__main__":
   multiple()