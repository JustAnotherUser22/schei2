
from turtle import shape
import numpy as np
import tensorflow as tf
from keras import models
from keras import layers
import random

def getNumberOfElementFromShape(shape):
   if(len(shape) == 2):
      return shape[0] * shape[1]
   elif(len(shape) == 1):
      return shape[0]
   else:
      return -1

def fromNetworkToArray(network):
   
   numberOfLayers = len(network.layers)
   numberOfEntry = numberOfLayers * 2  #ogni layer ha 2 valori: il vettore dei pesi e il vettore del bias
   array = np.array(666)
   shapeArray = []

   for i in range(0, numberOfEntry):
      layer = network.get_weights()[i]      
      array = np.append(array, layer)
      shapeArray.append(layer.shape)

   #print(array)
   array = np.delete(array, 0)
   #print(array)
   return (array, shapeArray)

   #vedi anche 
   #https://www.codespeedy.com/get_weights-and-set_weights-functions-in-keras-layers/

   for i in range(0, numberOfLayers):
      index = i*2
      numberOfElement = getNumberOfElementFromShape(shapeArray[index])
      tmp1 = array[:numberOfElement]
      tmp1 = np.array(tmp1)
      tmp1 = tmp1.reshape(shapeArray[index])
      tmp1 = np.full(tmp1.shape, fill_value = index)
      array = array[numberOfElement:]

      index = i*2+1
      numberOfElement = getNumberOfElementFromShape(shapeArray[index])
      tmp2 = array[:numberOfElement]
      tmp2 = np.array(tmp2)
      tmp2 = tmp2.reshape(shapeArray[index])
      tmp2 = np.full(tmp2.shape, fill_value = index)
      array = array[numberOfElement:]

      tmp = [tmp1, tmp2]
      network.layers[i].set_weights(tmp)

   print(network.summary())
   return
   
def fromArrayToNetwork(network, array, shapeArray):
   numberOfLayers = len(network.layers)
   for i in range(0, numberOfLayers):
      index = i*2
      numberOfElement = getNumberOfElementFromShape(shapeArray[index])
      tmp1 = array[:numberOfElement]
      tmp1 = np.array(tmp1)
      tmp1 = tmp1.reshape(shapeArray[index])
      #tmp1 = np.full(tmp1.shape, fill_value = index)
      array = array[numberOfElement:]

      index = i*2+1
      numberOfElement = getNumberOfElementFromShape(shapeArray[index])
      tmp2 = array[:numberOfElement]
      tmp2 = np.array(tmp2)
      tmp2 = tmp2.reshape(shapeArray[index])
      #tmp2 = np.full(tmp2.shape, fill_value = index)
      array = array[numberOfElement:]

      tmp = [tmp1, tmp2]
      network.layers[i].set_weights(tmp)

   #print(network.summary())
   return

def crossArray(array1, array2, ricombinationProbability, crossProbability):
   
   if(len(array1) != len(array2)):
      print("ERROR")
      return
   
   for i in range(1, len(array1)):
      n = random.randint(0, 100)
      #if(n >= 90):
      if(n >= ricombinationProbability):
         array1[i] = array2[i]
      else:
         n = random.randint(0, 100)
         #if(n >= 90):
         if(n >= crossProbability):
            #array1[i] = (random.randint(-10000, 10000) / 10000)  # [-1, 1]
            array1[i] = (random.randint(-200000000, 200000000) / 100000000)  # [-2, 2]
            #n = random.randint(-100, 100) / 1000000
            #array1[i] = array1[i] + float(n)

def plotTest():
   import matplotlib.pyplot as plt
   
   value = [1,2,3,4,5,6,7,8,9,10]

   epochs = range(1, len(value) + 1)
   plt.plot(epochs, value, 'r', label='Training loss')
   plt.title('Training and validation loss')
   plt.xlabel('Epochs')
   plt.ylabel('Loss')
   plt.legend()
   plt.show()


def main():

   plotTest()


   network = models.Sequential()
   network.add(layers.Dense(2, activation='relu', input_shape=(2,) ))
   network.add(layers.Dense(3))
   network.add(layers.Dense(1))
   network.summary()
   print(len(network.layers))

   (a, b) = fromNetworkToArray(network)
   fromArrayToNetwork(network, a, b)
   print(network.get_weights())
   print(network.layers[0].get_weights())

   """
   v = np.array( [[1, 2], [3, 4]] )
   print(v)

   a = np.append(v[0], v[1])
   print(a)

   print(v.shape)
   b = v.reshape( (4,1) )
   print(b)
   c = b.reshape( (2,2) )
   print(c)
   """

   a = [1,2,3,4,5,6,7,8,9,10]
   b = [11,12,13,14,15,16,17,18,19,20]
   crossArray(a, b)
   print(a, b)

if __name__ == "__main__":
   main()