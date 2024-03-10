
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import random

#note:
#sequenceLength = 1000  ->  2s per epoch
#sequenceLength = 10000 -> 16s per epoch
#batch_size = 1 -> uso tutti i dati disponibili (??????)


def createSequenceOfNumbers(length):
   x = []
   y = []
   
   random.seed(42)

   for i in range(length):
      x.append([random.randrange(1, 5, 1), random.randrange(1, 5, 1)])

   for entry in x:
      if(entry[1] == 2 * entry[0]):
         y.append(1)
      else:
         y.append(0)

   return x, y
   



def main():
   sequenceLength = 10000
   x, y = createSequenceOfNumbers(sequenceLength)
   x = np.array(x)
   y = np.array(y)

   x = x.reshape(sequenceLength, 2, 1)
   y = y.reshape(sequenceLength, 1)
   print(x.shape)
   print(y.shape)

   model = tf.keras.models.Sequential()
   model.add(tf.keras.layers.LSTM(5, input_shape=(2, 1)))
   model.add(tf.keras.layers.Dense(1))
   model.compile(loss='mean_squared_error', optimizer='adam')
   model.fit(x, 
             y, 
             epochs = 10, 
             batch_size = 1, 
             verbose = 2)

   entry = np.array([[[1],[1]]])
   result = model.predict(entry)
   print(entry.shape)
   print(result.shape)

   print(result)




   

if __name__ == "__main__":
   main()
