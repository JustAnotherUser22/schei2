import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from keras import models
from keras import layers

"""
script che esegue il training di una NN 
dopo aver caricato un file con questa struttura:
   feature 1      feature 2         result
   primo numero   secondo numero    somma
la NN poi prova a predirre il risultato della somma di due numeri
passati al termine della fase di training
"""

def printHistoryData(history):
   history_dict = history.history
   print(history_dict.keys())

   loss_values = history_dict['loss']
   val_loss_values = history_dict['val_loss']
   #epochs = range(1, 500 + 1)
   epochs = range(1, len(val_loss_values) + 1)
   plt.plot(epochs, loss_values, 'r', label='Training loss')
   plt.plot(epochs, val_loss_values, 'b', label='Validation loss')
   plt.title('Training and validation loss')
   plt.xlabel('Epochs')
   plt.ylabel('Loss')
   plt.legend()
   plt.show()

def readData():
   inputFileName = "D:/script/sum.csv"
   file = open(inputFileName, 'r')
   data = file.read()
   data = data.split('\n')
   file.close()
   return data

class haltCallback(tf.keras.callbacks.Callback):
   def on_epoch_end(self, epoch, logs={}):
      if(logs.get('loss') <= 0.5):
         print("\n\n\nReached 0.05 loss value so cancelling training!\n\n\n")
         self.model.stop_training = True


def main():
   data = readData()

   header = data[0]
   lines = data[1:]

   for i in range (0, len(lines)):
      lines[i] = lines[i].replace(',','.')

   #lines = data.split('\n')
   print("number of line = " + str(len(lines)))
   input = np.zeros( (len(lines), 2) )
   output = np.zeros( (len(lines), 1) )

   for i, line in enumerate(lines):
      values = [float(x) for x in line.split(';')[0:2]]
      input[i, :] = values
      data = line.split(';')[2]
      if(data == "END"):
         output[i, :] = 0
      else:
         output[i, :] = data
      
   print("input shape = " + str(input.shape))
   print("output shape = " + str(output.shape))

   network = models.Sequential()
   network.add(layers.Dense(2, activation='relu', input_shape=(2,)))
   #network.add(layers.Dense(5, activation='relu'))
   #network.add(layers.Dense(2, activation='relu'))
   network.add(layers.Dense(1))

   network.summary()

   test = np.array([ [15.21, 35.44],
                     [77.6, 11.3] ])
   test_output = np.array( [50.65, 88.9] )

   #non so perchè, ma se voglio usare un solo dato devo formattarlo così...
   #test = np.array( [[15.21, 35.44]] )
   #test_output = np.array( [50.65] )

   network.compile(optimizer='rmsprop', loss='mse', metrics=['mae'])

   history = network.fit(input, 
                        output, 
                        epochs = 1000, 
                        batch_size = 50, 
                        validation_data = (test, test_output) , 
                        callbacks=[haltCallback()] )

   printHistoryData(history)

   print("test shape = " + str(test.shape))

   prediction = network.predict(test)
   print(prediction)
   print(network.predict(test))
   print(network.get_weights())



if __name__ == "__main__":
   main()