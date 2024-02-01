
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from ta.trend import SMAIndicator
from keras import models
from keras import layers
import tensorflow as tf

import sys
sys.path.insert(1, "schei2/EURUSD/dataFolder")
import dataFiles

PATH = "schei2\detectGoodRegions\data.csv"

ENTER_POSITIVE = 0
DO_NOTHING = 1
ENTER_NEGATIVE = 2



def GenerateFile():

   timestamp = 0
   value = 1
   #if(os.path.exists(path)):
   #   pass
   f = open(PATH, 'w')
   f.write("timestamp,value\n")

   for i in range(100):
      timestamp += 1
      value = 1
      string = "{0}, {1}\n".format(timestamp, round(value, 3))
      f.write(string)

   for i in range(30):
      timestamp += 1
      value = value + 0.001
      string = "{0}, {1}\n".format(timestamp, round(value, 3))
      f.write(string)

   for i in range(300):
      timestamp += 1
      value = value - 0.001
      string = "{0}, {1}\n".format(timestamp, round(value, 3))
      f.write(string)

   for i in range(30):
      timestamp += 1
      value = value + 0.001
      string = "{0}, {1}\n".format(timestamp, round(value, 3))
      f.write(string)

   for i in range(100):
      timestamp += 1
      string = "{0}, {1}\n".format(timestamp, round(value, 3))
      f.write(string)


   f.close()

def addExpectedClassForAllData():
   file = pd.read_csv(PATH)

   (numberOfRows, numberOfCloumn) = file.shape
   file.insert(numberOfCloumn, "class", [DO_NOTHING] * numberOfRows)

   file["class"] = np.where(file["value"] > 1.005, ENTER_POSITIVE, file["class"])
   file["class"] = np.where(file["value"] < 0.76, ENTER_NEGATIVE, file["class"])

   print(file)
   return file



def addFeature(file):
   file, featureNames = addOnlySmaToDatabase(file)
   file = file.dropna()

# preallocate empty array and assign slice by chrisaycock
def shift5(arr, num, fill_value=np.nan):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = fill_value
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = fill_value
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result

def addPreviousData(data):
   inputData = data["value"]
   featureNames = []
   length = len(inputData)

   start = 1
   stop = 40
   step = 1

   for i in range(start, stop, step):
      name = "back_{0}".format(i)
      dataToAdd = inputData.copy()
      dataToAdd = shift5(dataToAdd, i)
      df = pd.DataFrame(dataToAdd, columns = [name])
      data = pd.concat([data, df], axis = 1, names = [list(data.columns), name])

   return data


def addOnlySmaToDatabase(data):
   inputData = data["value"]
   #inputData = data.loc[:, "value"]

   featureNames = []

   start = 1
   stop = 40
   step = 1
   for i in range(start, stop, step):
      sma = SMAIndicator(close = inputData, window = i)
      sma = np.array(sma.sma_indicator())
      name = "sma_{0}".format(i)
      
      #il compilatore si lamenta che questo è lento
      #data.insert(1, name, ema)
      featureNames.append(name)

      #più veloceeeeee!!
      df = pd.DataFrame(sma, columns = [name])
      data = pd.concat([data, df], axis = 1, names = [list(data.columns), name])
   
   return data, featureNames


def implementNN(X, y_real):
   
   y_real = tf.keras.utils.to_categorical(y_real, num_classes = 3)

   (xRow, xColumn) = X.shape

   network = models.Sequential()
   network.add(layers.Dense(2, activation = 'relu', input_shape = (xColumn, ) ))
   network.add(layers.Dense(30, activation = 'relu'))
   network.add(layers.Dense(25, activation = 'relu'))
   network.add(layers.Dense(20, activation = 'relu'))
   network.add(layers.Dense(10, activation = 'relu'))
   network.add(layers.Dense(5, activation = 'relu'))
   network.add(layers.Dense(3, activation = 'softmax'))

   network.summary()

   #network.compile(loss="categorical_crossentropy", optimizer= "adam", metrics=['accuracy'])
   network.compile(loss="categorical_crossentropy", optimizer= "adam", metrics=['accuracy', tf.keras.metrics.Precision(), tf.keras.metrics.Recall(), tf.keras.metrics.FalsePositives(), tf.keras.metrics.FalseNegatives()])

   history = network.fit(X,
                         y_real, 
                         epochs = 200, 
                         #batch_size = 50, 
                         )
   
   printHistoryData(history)

   return network


def main():
   GenerateFile()
   file = addExpectedClassForAllData()
   file.to_csv(PATH, index = False)

   file = pd.read_csv(PATH)
   print(file)

   numberOf1 = len(file[file["class"] == ENTER_POSITIVE])
   numberOf0 = len(file[file["class"] == DO_NOTHING])
   numberOfNo1 = len(file[file["class"] == ENTER_NEGATIVE])

   print(numberOf1)
   print(numberOf0)
   print(numberOfNo1)

   #addFeature(file)
   file = addPreviousData(file)
   file = file.dropna()
   print(file)

   X = file.drop(columns = ["timestamp", "class"])
   y_real = file["class"]

   model = implementNN(X, y_real)   

   y_predict = model.predict(X)

   plt.plot(y_real)
   y_predict = np.argmax(y_predict, axis = 1)
   print(y_predict)
   #plt.show()


def printHistoryData(history):
   history_dict = history.history
   print(history_dict.keys())

   loss_values = history_dict['loss']
   accuracy_values = history_dict['accuracy']
   precision = history_dict['precision']
   recall = history_dict['recall']
   false_negatives = history_dict['false_negatives']
   false_positives = history_dict['false_positives']
   
   #epochs = range(1, 500 + 1)
   epochs = range(1, len(accuracy_values) + 1)
   #plt.plot(epochs, loss_values, 'r', label='Training loss')
   #plt.plot(epochs, accuracy_values, 'b', label='accuracy')
   #plt.plot(epochs, precision, 'g', label = 'precison')
   #plt.plot(epochs, recall, 'k', label = 'recall')
   plt.plot(epochs, false_negatives, 'r', label = 'false negatives')
   plt.plot(epochs, false_positives, 'b', label = 'false positives')
   
   plt.title('Training and validation loss')
   plt.xlabel('Epochs')
   plt.ylabel('Loss')
   plt.legend()
   plt.show()


if __name__ == "__main__":
   #main()

   file = pd.read_csv(dataFiles.BASE_PATH + dataFiles.FILE_2022_1M_FORMATTED)
   print(file)
   print(file.columns)

   #value = file["Bar OPEN Bid Quote"]
   #print(value)
   
   #plt.plot(value[412 : 412 + 3600])
   #plt.show()
   
