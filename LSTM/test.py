
'''
le lstm nascono per gestire dati temporali
provo a vedere cosa succede
'''

import sys
sys.path.insert(1, "schei2/EURUSD/dataFolder")
import dataFiles
import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def create_sequences(data, seq_length):
    X = []
    y = []
    l = len(data)
    for i in range(l - seq_length):
        X.append(data[i:i+seq_length])
        y.append(data[i+seq_length])        
    return np.array(X), np.array(y)


def main():
   filePath = dataFiles.BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_window_100.csv"
   lines = pd.read_csv(filePath)
   
   dati = lines.iloc[:, 1]
   #predict = []
   #predict.insert(len(predict) - 1, predict.pop(0))
   
   dati = dati[0 : 10000]

   trainDimension = int(len(dati) * 0.95)
   
   train_data = dati[:trainDimension]
   test_data  = dati[trainDimension:]
   train_data = np.array(train_data)
   test_data = np.array(test_data)
   #print(test_data)

   seq_length = 20
   testDimension = len(dati) - trainDimension - seq_length
   
   X_test, y_test = create_sequences(test_data, seq_length)
   X_train, y_train = create_sequences(train_data, seq_length)
   
   X_train = X_train.reshape((X_train.shape[0], X_train.shape[1], 1))
   X_test = X_test.reshape((X_test.shape[0], X_test.shape[1], 1))
   y_train = y_train.reshape((y_train.shape[0], 1))
   y_test = y_test.reshape((y_test.shape[0], 1))
   print(X_train.shape)
   print(y_train.shape)
   
   '''
   model = tf.keras.models.Sequential()
   model.add(tf.keras.layers.LSTM(units=128, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
   #model.add(tf.keras.layers.LSTM(units=64, return_sequences=True))
   #model.add(tf.keras.layers.LSTM(units=64, return_sequences=True))
   model.add(tf.keras.layers.Dense(units=1))
   model.compile(loss='mean_squared_error', optimizer='adam')
   
   history = model.fit(X_train, 
                       y_train, 
                       epochs = 2,#10, 
                       batch_size = 1, 
                       verbose = 2, 
                       validation_data = (X_test, y_test))
   '''
   model = tf.keras.models.Sequential()
   model.add(tf.keras.layers.LSTM(128, return_sequences=True, input_shape=(X_train.shape[1], X_train.shape[2])))
   model.add(tf.keras.layers.LSTM(64, return_sequences=True))
   model.add(tf.keras.layers.LSTM(64))
   model.add(tf.keras.layers.Dense(1))
   model.compile(loss='mean_squared_error', optimizer='adam')
   history = model.fit(X_train, 
                       y_train, 
                       epochs = 10, 
                       batch_size = 1, 
                       verbose = 2, 
                       validation_data = (X_test, y_test)
                       )

   #plt.plot(history.history['loss'], 'r')
   #plt.plot(history.history['val_loss'], 'k')
   #plt.show()

   '''
   entry = [1.1, 1.1, 1.2, 1.2, 1.3]
   entry = np.array(entry)
   entry = entry.reshape(1, 5, 1)
   print(entry)
   predict = model.predict(entry)
   print(predict)
   '''

   pred = model.predict(X_test)

   diff = pred - y_test
   diff = diff**2
   diff = diff / 950

   #pred = []
   #for i in range(X_test.shape[0]):
   #   entry = X_test[i, :, :]
   #   entry = np.array(entry)
   #   entry = entry.reshape(1, seq_length, 1)   
   #   predict = model.predict(entry)
   #   pred.append(predict)
   
   #pred = np.array(pred)
   #pred = pred.reshape(950, 1)
   plt.plot(pred, color='k')
   plt.plot(y_test, color='b')
   plt.show()

   a = 0


def porocd():
   X = np.array([
        [5.,0.,-4.,3.,2.],
        [2.,-12.,1.,0.,0.],
        [0.,0.,13.,0.,-13.],
        [87.,-40.,2.,1.,0.]
    ])
   X = X.reshape(4, 5, 1)
   y = np.array([[6.],[-9.],[0.],[50.]])

   print(X.shape)
   print(y.shape)

   model = tf.keras.models.Sequential()
   model.add(tf.keras.layers.LSTM(5, input_shape=(5, 1)))
   model.add(tf.keras.layers.Dense(1))
   model.compile(loss='mean_squared_error', optimizer='adam')
   model.fit(X, y, epochs=1000, batch_size=4, verbose=0)

   entry = np.array([[[0.],[0.],[0.],[0.],[0.]]])
   result = model.predict(entry)
   print(entry.shape)
   print(result.shape)
   print(result)
   print(model.predict(np.array([[[10.],[-10.],[10.],[-10.],[0.]]])))
   print(model.predict(np.array([[[10.],[20.],[30.],[40.],[50.]]])))

   

if __name__ == "__main__":
   main()
   #porocd()  