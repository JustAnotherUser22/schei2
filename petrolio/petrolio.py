
import yfinance as yf
import numpy as np
import tensorflow
import matplotlib.pyplot as plt
import pandas_ta as ta
import pandas as pd

def NormalizeArray(array):
   max = np.max(array)
   return array / max, max

def NormalizeMatrix(matrix):
   matrix = np.array(matrix)
   nRow = matrix.shape[0]
   nCol = matrix.shape[1]
   max = np.zeros( (1, nCol) )
   for i in range(nCol):
      p, d = NormalizeArray(matrix[:, i])
      #matrix[:, i], max[1, i] = NormalizeArray(matrix[:, i])
      matrix[:, i] = p 
      max[0, i] = d
   return matrix, max

def downloadAndSave():
    data = yf.download(tickers = "LCO", start = "2012-03-11", end = "2022-07-10")
    print(data.head(5))
    f = open("invest.txt", "a")

    a = data.shape[0]
    b = data.shape[1]
    data = np.array(data)

    for i in range(a):
        line = data[i]
        line = str(line)
        line = line.replace('\n', '')
        line = line.replace('[', '')
        line = line.replace(']', '')
        line = line + '\n'
        f.write(line)
    f.close()

def Load():
   
   matrix = []

   path = "C:/Users/Marco/Documents/python/petrolio/Future Petrolio Brent Dati Storici.csv"
   f = open(path, 'r')
   lines = f.readlines()
   for i in range(1, len(lines)):
      data = lines[i].split("\",\"")
      array = []
      n = data[1].replace('\'', '')
      array.append(float(data[1].replace('\'', '').replace(',','.')))
      array.append(float(data[2].replace('\'', '').replace(',','.')))
      array.append(float(data[3].replace('\'', '').replace(',','.')))
      array.append(float(data[4].replace('\'', '').replace(',','.')))
      matrix.append(array)
   
   matrix.remove(matrix[0])   #tolgo prima riga

   matrix = np.array(matrix)

   return matrix

def main():
   data = Load()
   #data = np.reshape(data, (len(data), 1))
   data, max = NormalizeMatrix(data)

   currentData = data[:, 0]
   nextData = data[1:, 0]
   nextData = np.append(nextData, [0])
   delta = nextData - currentData

   data = np.append(data, delta, axis = 1)

   l = 30

   #nRow = data.shape[0]
   #nCol = data.shape[1]
  
   y = data[l+1:, 0]
   #y = y[1:]   #rimuovi primo elemento, perchè devo predirre il valore successivo

   data = np.delete(data, (data.shape[0]-1), axis = 0)

   nRow = data.shape[0]
   nCol = data.shape[1]
   
   x = []
   for i in range(l, nRow):
      x.append(data[ i-l:i, :])

   x = np.array(x)
   #x = np.delete(x, (x.shape[0]), axis = 0)
   X = x

   print("post process dim")
   print(x.shape)
   print(x.ndim)
   print(y.shape)
   print(y.ndim)

   splitlimit = int(len(X)*0.95)
   X_train, X_test = X[:splitlimit], X[splitlimit:]
   y_train, y_test = y[:splitlimit], y[splitlimit:]

   X_train = np.array(X_train)
   X_test = np.array(X_test)
   y_train = np.array(y_train)
   y_test = np.array(y_test)

   y_train = np.reshape(y_train, (len(y_train), 1) )
   y_test = np.reshape(y_test, (len(y_test), 1) )
   print(X_train.shape)
   print(X_test.shape)
   print(y_train.shape)
   print(y_test.shape)
   print(y_train)

   model = tensorflow.keras.models.Sequential([
      tensorflow.keras.layers.LSTM(5, name='first_layer', input_shape = (l, nCol)),
      tensorflow.keras.layers.Dense(1, activation = "linear")
   ])

   adam = tensorflow.keras.optimizers.Adam()
   rms = tensorflow.keras.optimizers.RMSprop()
   model.compile(optimizer = adam, 
                  loss = 'mse' )

   localTrainLoss = []
   localTestLoss = []
   lastTrainLoss = 0
   lastTestLoss = 0
   '''
   plt.ion()
   plt.show()
   plt.cla()
   plt.clf()
   plt.title('Training and validation loss')
   plt.xlabel('Epochs')
   plt.ylabel('Loss')
   #plt.legend()
   '''

   history = model.fit(x = X_train, 
                        y = y_train, 
                        batch_size = 15, 
                        epochs = 30, 
                        shuffle = True, 
                        validation_split = 0.1, 
                        #callbacks = [trainingStopCallback],
                        verbose = 1)
   
   history_dict = history.history
   loss_values = history_dict['loss']
   val_loss_values = history_dict['val_loss']

   #globalTrainLoss.append(loss_values)
   localTrainLoss += loss_values
   #globalTestLoss.append(val_loss_values)
   localTestLoss += val_loss_values
   '''
   epochs = range(1, len(localTrainLoss) + 1)
   plt.plot(epochs, localTrainLoss, 'b', label='Training loss')
   plt.plot(epochs, localTestLoss, 'r', label='Validation loss')
   plt.draw()
   plt.pause(0.001)
   plt.show()
   '''
   y_pred = model.predict(X_test)
   delta = []
   for i in range(len(y_pred)):
      proportional = float(max[0,0])
      prediction = float(y_pred[i]) * proportional
      real = float(y_test[i]) * proportional
      print("{:.2f} {:.2f}".format(prediction, real))
      delta.append(abs(prediction-real))

   plt.plot(y_pred, 'r')
   plt.plot(y_test, 'b')
   plt.show()

def ComputeNextClose():
   data = Load()
   data, max = NormalizeMatrix(data)

   l = 30

   #nRow = data.shape[0]
   #nCol = data.shape[1]
  
   y = data[l+1:, 0]
   #y = y[1:]   #rimuovi primo elemento, perchè devo predirre il valore successivo

   data = np.delete(data, (data.shape[0]-1), axis = 0)

   nRow = data.shape[0]
   nCol = data.shape[1]
   
   x = []
   for i in range(l, nRow):
      x.append(data[ i-l:i, :])

   x = np.array(x)
   #x = np.delete(x, (x.shape[0]), axis = 0)
   X = x

   print("post process dim")
   print(x.shape)
   print(x.ndim)
   print(y.shape)
   print(y.ndim)

   splitlimit = int(len(X)*0.95)
   X_train, X_test = X[:splitlimit], X[splitlimit:]
   y_train, y_test = y[:splitlimit], y[splitlimit:]

   X_train = np.array(X_train)
   X_test = np.array(X_test)
   y_train = np.array(y_train)
   y_test = np.array(y_test)

   y_train = np.reshape(y_train, (len(y_train), 1) )
   y_test = np.reshape(y_test, (len(y_test), 1) )
   print(X_train.shape)
   print(X_test.shape)
   print(y_train.shape)
   print(y_test.shape)
   print(y_train)

   model = tensorflow.keras.models.Sequential([
      tensorflow.keras.layers.LSTM(5, name='first_layer', input_shape = (l, nCol)),
      tensorflow.keras.layers.Dense(1, activation = "linear")
   ])

   adam = tensorflow.keras.optimizers.Adam()
   rms = tensorflow.keras.optimizers.RMSprop()
   model.compile(optimizer = adam, 
                  loss = 'mse' )

   localTrainLoss = []
   localTestLoss = []
   lastTrainLoss = 0
   lastTestLoss = 0
   '''
   plt.ion()
   plt.show()
   plt.cla()
   plt.clf()
   plt.title('Training and validation loss')
   plt.xlabel('Epochs')
   plt.ylabel('Loss')
   #plt.legend()
   '''

   history = model.fit(x = X_train, 
                        y = y_train, 
                        batch_size = 15, 
                        epochs = 30, 
                        shuffle = True, 
                        validation_split = 0.1, 
                        #callbacks = [trainingStopCallback],
                        verbose = 1)
   
   history_dict = history.history
   loss_values = history_dict['loss']
   val_loss_values = history_dict['val_loss']

   #globalTrainLoss.append(loss_values)
   localTrainLoss += loss_values
   #globalTestLoss.append(val_loss_values)
   localTestLoss += val_loss_values
   '''
   epochs = range(1, len(localTrainLoss) + 1)
   plt.plot(epochs, localTrainLoss, 'b', label='Training loss')
   plt.plot(epochs, localTestLoss, 'r', label='Validation loss')
   plt.draw()
   plt.pause(0.001)
   plt.show()
   '''
   y_pred = model.predict(X_test)
   delta = []
   for i in range(len(y_pred)):
      proportional = float(max[0,0])
      prediction = float(y_pred[i]) * proportional
      real = float(y_test[i]) * proportional
      print("{:.2f} {:.2f}".format(prediction, real))
      delta.append(abs(prediction-real))

   plt.plot(y_pred, 'r')
   plt.plot(y_test, 'b')
   plt.show()


def ComputeRSIFormData(data, n):
   df = pd.DataFrame(data, columns = ['a'])
   porcodio = ta.rsi(df.a, length = 6)
   porcodio = np.array(porcodio)
   porcodio = np.reshape(porcodio, (len(porcodio), 1))
   return porcodio

def ComputeSMAFormData(data, n):
   df = pd.DataFrame(data, columns = ['a'])
   porcodio = ta.sma(df.a, length = 6)
   porcodio = np.array(porcodio)
   porcodio = np.reshape(porcodio, (len(porcodio), 1))
   return porcodio

def SplitData(X, y):
   splitlimit = int(len(X)*0.95)
   X_train, X_test = X[:splitlimit], X[splitlimit:]
   y_train, y_test = y[:splitlimit], y[splitlimit:]

   X_train = np.array(X_train)
   X_test = np.array(X_test)
   y_train = np.array(y_train)
   y_test = np.array(y_test)

   y_train = np.reshape(y_train, (len(y_train), 1) )
   y_test = np.reshape(y_test, (len(y_test), 1) )
   print(X_train.shape)
   print(X_test.shape)
   print(y_train.shape)
   print(y_test.shape)
   print(y_train)

   return X_train, X_test, y_train, y_test

def GetFeaturesAndResultFromData(data, l):
   
   nRow = data.shape[0]
   nCol = data.shape[1]
  
   y = data[l+1:, -1]
   #y = y[1:]   #rimuovi primo elemento, perchè devo predirre il valore successivo

   #data = np.split(data, data.shape[1]-1, axis = 0)
   data = data[:, 0:nCol-1]
   data = np.delete(data, (data.shape[0]-1), axis = 0) #cancello ultima riga

   nRow = data.shape[0]
   nCol = data.shape[1]
   
   x = []
   for i in range(l, nRow):
      x.append(data[ i-l:i, :])

   x = np.array(x)
   #x = np.delete(x, (x.shape[0]), axis = 0)
   X = x

   print("post process dim")
   print(x.shape)
   print(x.ndim)
   print(y.shape)
   print(y.ndim)

   return x, y, data

def ComputeNextDelta():
   data = Load()
   data, max = NormalizeMatrix(data)

   currentData = data[:, 0]
   nextData = data[1:, 0]
   nextData = np.append(nextData, [0])
   delta = nextData - currentData
   delta = np.reshape(delta, (len(delta), 1))

   #data = np.append(data, delta, axis = 1)
   
   rsi_6 = ComputeRSIFormData(currentData, 6)
   rsi_5 = ComputeRSIFormData(currentData, 5)
   rsi_4 = ComputeRSIFormData(currentData, 4)
   rsi_3 = ComputeRSIFormData(currentData, 3)
   rsi_2 = ComputeRSIFormData(currentData, 2)

   sma_6 = ComputeSMAFormData(currentData, 6)
   sma_5 = ComputeSMAFormData(currentData, 5)
   sma_4 = ComputeSMAFormData(currentData, 4)
   sma_3 = ComputeSMAFormData(currentData, 3)
   sma_2 = ComputeSMAFormData(currentData, 2)
   
   data = np.append(data, rsi_6, axis = 1)
   data = np.append(data, rsi_5, axis = 1)
   data = np.append(data, rsi_4, axis = 1)
   data = np.append(data, rsi_3, axis = 1)
   data = np.append(data, rsi_2, axis = 1)

   data = np.append(data, sma_6, axis = 1)
   data = np.append(data, sma_5, axis = 1)
   data = np.append(data, sma_4, axis = 1)
   data = np.append(data, sma_3, axis = 1)
   data = np.append(data, sma_2, axis = 1)

   data = np.append(data, delta, axis = 1)

   data = data[~np.isnan(data).any(axis=1)]  #rimuove valori NaN
   
   l = 30

   nRow = data.shape[0]
   nCol = data.shape[1]
  
   y = data[l+1:, -1]
   #y = y[1:]   #rimuovi primo elemento, perchè devo predirre il valore successivo

   #data = np.split(data, data.shape[1]-1, axis = 0)
   data = data[:, 0:nCol-1]
   data = np.delete(data, (data.shape[0]-1), axis = 0) #cancello ultima riga

   nRow = data.shape[0]
   nCol = data.shape[1]
   
   x = []
   for i in range(l, nRow):
      x.append(data[ i-l:i, :])

   x = np.array(x)
   #x = np.delete(x, (x.shape[0]), axis = 0)
   X = x

   print("post process dim")
   print(x.shape)
   print(x.ndim)
   print(y.shape)
   print(y.ndim)

   splitlimit = int(len(X)*0.95)
   X_train, X_test = X[:splitlimit], X[splitlimit:]
   y_train, y_test = y[:splitlimit], y[splitlimit:]

   X_train = np.array(X_train)
   X_test = np.array(X_test)
   y_train = np.array(y_train)
   y_test = np.array(y_test)

   y_train = np.reshape(y_train, (len(y_train), 1) )
   y_test = np.reshape(y_test, (len(y_test), 1) )
   print(X_train.shape)
   print(X_test.shape)
   print(y_train.shape)
   print(y_test.shape)
   print(y_train)

   model = tensorflow.keras.models.Sequential([
      tensorflow.keras.layers.LSTM(5, name='first_layer', input_shape = (l, nCol)),
      tensorflow.keras.layers.Dense(1, activation = "linear")
   ])

   adam = tensorflow.keras.optimizers.Adam()
   rms = tensorflow.keras.optimizers.RMSprop()
   model.compile(optimizer = adam, 
                  loss = 'mse' )

   localTrainLoss = []
   localTestLoss = []

   history = model.fit(x = X_train, 
                        y = y_train, 
                        batch_size = 15, 
                        epochs = 30, 
                        shuffle = True, 
                        validation_split = 0.1, 
                        #callbacks = [trainingStopCallback],
                        verbose = 1)
   
   history_dict = history.history
   loss_values = history_dict['loss']
   val_loss_values = history_dict['val_loss']

   #globalTrainLoss.append(loss_values)
   localTrainLoss += loss_values
   #globalTestLoss.append(val_loss_values)
   localTestLoss += val_loss_values

   y_pred = model.predict(X_test)
   delta = []
   for i in range(len(y_pred)):
      proportional = float(max[0,0])
      prediction = float(y_pred[i]) * proportional
      real = float(y_test[i]) * proportional
      print("{:.2f} {:.2f}".format(prediction, real))
      delta.append(abs(prediction-real))

   plt.plot(y_pred, 'r')
   plt.plot(y_test, 'b')
   plt.show()

def ComputeNextClass():
   data = Load()
   data, max = NormalizeMatrix(data)

   currentData = data[:, 0]
   nextData = data[1:, 0]
   nextData = np.append(nextData, [0])
   delta = nextData - currentData
   delta = np.reshape(delta, (len(delta), 1))

   cathegory = delta
   for i in range(len(cathegory)):
      if(cathegory[i] > 0):
         cathegory[i] = 1
      else:
         cathegory[i] = 0

   rsi_6 = ComputeRSIFormData(currentData, 6)
   rsi_5 = ComputeRSIFormData(currentData, 5)
   rsi_4 = ComputeRSIFormData(currentData, 4)
   rsi_3 = ComputeRSIFormData(currentData, 3)
   rsi_2 = ComputeRSIFormData(currentData, 2)
   sma_11 = ComputeSMAFormData(currentData, 11)
   sma_10 = ComputeSMAFormData(currentData, 10)
   sma_9 = ComputeSMAFormData(currentData, 9)
   sma_8 = ComputeSMAFormData(currentData, 8)
   sma_7 = ComputeSMAFormData(currentData, 7)   
   sma_6 = ComputeSMAFormData(currentData, 6)
   sma_5 = ComputeSMAFormData(currentData, 5)
   sma_4 = ComputeSMAFormData(currentData, 4)
   sma_3 = ComputeSMAFormData(currentData, 3)
   sma_2 = ComputeSMAFormData(currentData, 2)   
   data = np.append(data, rsi_6, axis = 1)
   data = np.append(data, rsi_5, axis = 1)
   data = np.append(data, rsi_4, axis = 1)
   data = np.append(data, rsi_3, axis = 1)
   data = np.append(data, rsi_2, axis = 1)
   data = np.append(data, sma_11, axis = 1)
   data = np.append(data, sma_10, axis = 1)
   data = np.append(data, sma_9, axis = 1)
   data = np.append(data, sma_8, axis = 1)
   data = np.append(data, sma_7, axis = 1)
   data = np.append(data, sma_6, axis = 1)
   data = np.append(data, sma_5, axis = 1)
   data = np.append(data, sma_4, axis = 1)
   data = np.append(data, sma_3, axis = 1)
   data = np.append(data, sma_2, axis = 1)

   data = np.append(data, cathegory, axis = 1)
   #data = np.append(data, delta, axis = 1)

   data = data[~np.isnan(data).any(axis=1)]  #rimuove valori NaN
   
   l = 30
   

   #X, y, data = GetFeaturesAndResultFromData(data, l)
   y = data[:, -1]
   X = data[:, 0:data.shape[1]-1]

   nCol = data.shape[1]

   X_train, X_test, y_train, y_test = SplitData(X, y)

   model = tensorflow.keras.models.Sequential([
      #tensorflow.keras.layers.LSTM(5, name='first_layer', input_shape = (l, nCol)),
      tensorflow.keras.layers.Dense(20, activation = "sigmoid"),
      tensorflow.keras.layers.Dense(15, activation = "sigmoid"),
      tensorflow.keras.layers.Dense(10, activation = "sigmoid"),
      tensorflow.keras.layers.Dense(5, activation = "sigmoid"),
      tensorflow.keras.layers.Dense(5, activation = "sigmoid"),
      tensorflow.keras.layers.Dense(1, activation = "sigmoid")
   ])

   adam = tensorflow.keras.optimizers.Adam()
   rms = tensorflow.keras.optimizers.RMSprop()
   #model.compile(optimizer = adam, loss = 'mse' )
   model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

   localTrainLoss = []
   localTestLoss = []

   history = model.fit(x = X_train, 
                        y = y_train, 
                        batch_size = 15, 
                        epochs = 30, 
                        shuffle = True, 
                        validation_split = 0.1, 
                        #callbacks = [trainingStopCallback],
                        verbose = 1)
   
   history_dict = history.history
   loss_values = history_dict['loss']
   val_loss_values = history_dict['val_loss']

   #globalTrainLoss.append(loss_values)
   localTrainLoss += loss_values
   #globalTestLoss.append(val_loss_values)
   localTestLoss += val_loss_values

   y_pred = model.predict(X_test)
   delta = []
   for i in range(len(y_pred)):
      proportional = float(max[0,0])
      prediction = float(y_pred[i])
      real = float(y_test[i])
      print("{:.2f} {:.2f}".format(prediction, real))
      delta.append(abs(prediction-real))

   plt.plot(y_pred, 'r')
   plt.plot(y_test, 'b')
   plt.show()

def plotData():
   data = Load()
   #help(ta.macd)

   close = data[:, 0]

   df = pd.DataFrame(close, columns = ['a'])
   porcodio = ta.macd(df.a, fast = 12, slow = 26, signal = 9)
   porcodio = np.array(porcodio)
   #porcodio = np.reshape(porcodio, (len(porcodio), 1))

   macd = porcodio[:, 0]
   histogram = porcodio[:, 1]
   signal = porcodio[:, 2]
   #delta = histogram - macd + signal  #ok porco dio almeno questo è 0

   plt.plot(macd, 'r')
   plt.plot(histogram, 'g')
   plt.plot(signal, 'b')
   plt.plot(close)
   plt.show()

   for fast in range(1, 20):
      for slow in range (fast, 30):
         for signal in range (0, 10):
            pass
   


if __name__ == "__main__":
   #downloadAndSave()
   #ComputeNextClass()
   plotData()