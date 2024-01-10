import pandas as pd
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import RandomForestClassifier
from ta.trend import MACD
from ta.trend import EMAIndicator
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator
from ta.momentum import AwesomeOscillatorIndicator
from ta.momentum import KAMAIndicator
import numpy as np
from sklearn import tree
import sklearn
from sklearn.inspection import permutation_importance
from pathlib import Path
import features
from datetime import datetime
import os
import joblib
import ta


'''
carica dei dati
aggiunge delle features scelte dall'utente
fa il train di una random forest
mostra valori e plot di alcuni dati relativi alle performance del modello appena creato
'''

BASE_PATH = "pandas/pandas/"
FILE_1M_ALL2022_WITH_CLASS = "DAT_ASCII_EURUSD_M1_2022_formatted_class.csv"
FILE_1M_ALL2022_ORIGNAL = "DAT_ASCII_EURUSD_M1_2022_formatted.csv"
FILE_1M_ALL2022_WINDOWS_100 = "DAT_ASCII_EURUSD_M1_2022_window_100.csv"

### data manager

def computeClass(data, realNumberOfDataToConsider, timeWindow):
   print("inizio definizione classi")
   for i in range(realNumberOfDataToConsider-1):
      currentElement = data.iloc[i]
      currentValue = currentElement[1]
      end = False

      for j in range(timeWindow):
         if(end == False):
            nextElement = data.iloc[i+j]
            nextValue = nextElement[1]

            if(nextValue > currentValue + 0.001):
               data.loc[i, "class"] = 1
               end = True
            #if(nextValue < currentValue - 0.001):
            #   data.loc[i, "class"] = -1
            #   end = True

def formatDatabase(data):
   (numberOfRows, numberOfColumns) = data.shape

   data.insert(numberOfColumns, "class", [0]*numberOfRows)
   
   numberOfDataToConsider = numberOfRows #1000
   #print(data.head())
   #print(data.shape)

   timeWindow = 100#500 #trova massimo o minimo entro questo valore di entry nel futuro
   realNumberOfDataToConsider = numberOfDataToConsider - timeWindow

   computeClass(data, realNumberOfDataToConsider, timeWindow)

   #NB index = false -> non aggiunge una prima colonna con indici
   #data.to_csv("pandas/DAT_ASCII_EURUSD_M1_2022_gennaio_class.csv", index = False)
   #data.to_csv("pandas/DAT_ASCII_EURUSD_M1_2022_formatted_class.csv", index = False)
   data.to_csv(BASE_PATH + FILE_1M_ALL2022_WINDOWS_100, index = False)


def formatDatabaseWritingLinesOneByOne(data):
   '''
   se il file è troppo grande non riesco a scriverlo tutto in una volta perchè mi
   manca spazio su disco
   no dio can non mi ricordo perchè ho fatto questa funzione
   '''
   index = 0
   #my_file = Path("pandas/DAT_ASCII_EURUSD_M1_2022_formatted_class.csv")
   my_file = Path(BASE_PATH + FILE_1M_ALL2022_WINDOWS_100)
   if my_file.is_file():
      #f = open("pandas/DAT_ASCII_EURUSD_M1_2022_formatted_class.csv", 'r')
      f = open(BASE_PATH + FILE_1M_ALL2022_WINDOWS_100, 'r')
      lines = f.readlines()
      f.close()
      index = len(lines)
   else:
      index = 0
      #f = open("pandas/DAT_ASCII_EURUSD_M1_2022_formatted_class.csv", 'w')
      f = open(BASE_PATH + FILE_1M_ALL2022_WINDOWS_100, 'w')
      header = data.columns
      header = list(header)
      line = ""
      for element in header:
         line = line + str(element) + ','
      line = line[0:len(line)-1]
      line = line + '\n'
      f.write(str(line))
      f.close()
  
   
   (numberOfRows, numberOfColumns) = data.shape

   data.insert(numberOfColumns, "class", [0]*numberOfRows)
   
   numberOfDataToConsider = numberOfRows #1000
   #print(data.head())
   #print(data.shape)

   #timeWindow = 500 #trova massimo o minimo entro questo valore di entry nel futuro
   timeWindow = 100 #trova massimo o minimo entro questo valore di entry nel futuro
   realNumberOfDataToConsider = numberOfDataToConsider - timeWindow

   for i in range(index, realNumberOfDataToConsider-1, 1):
      currentElement = data.iloc[i]
      currentValue = currentElement[1]
      end = False

      for j in range(timeWindow):
         if(end == False):
            nextElement = data.iloc[i+j]
            nextValue = nextElement[1]

            if(nextValue > currentValue + 0.001):
               data.loc[i, "class"] = 1
               end = True
            if(nextValue < currentValue - 0.001):
               data.loc[i, "class"] = -1
               end = True
      
      #f = open("pandas/DAT_ASCII_EURUSD_M1_2022_formatted_class.csv", 'a')
      f = open(BASE_PATH + FILE_1M_ALL2022_WINDOWS_100, 'a')
      entry = data.iloc[[i]].to_csv(header = False, index = False)      #con "to_csv" uso il carattere ',' come sepratore
      line = str(entry)
      line = line.replace("\r\n", '')
      line = line + '\n'
      f.write(line)
      f.close()

   #NB index = false -> non aggiunge una prima colonna con indici
   #data.to_csv("pandas/DAT_ASCII_EURUSD_M1_2022_formatted_class.csv", index = False)

def addTestFeatureToDatabase(data):
   inputData = data.iloc[:,1]

   featuresName = ["fast", "macd", "diff", "signal", \
                    'emaVerySlow', 'emaVerySlow-1', 'emaVerySlow-2', \
                     'emaSlow', 'emaSlow-1', 'emaSlow-2', \
                     'emaMedium', 'emaMedium-1', 'emaMedium-2', \
                     'emaFast', 'emaFast-1', 'emaFast-2', \
                     'rsi1', 'rsi2', 'rsi3']

   signal = MACD(close = inputData, window_slow = 26, window_fast = 15, window_sign = 9)
   #800 400 200 50
   emaVerySlow = EMAIndicator(close = inputData, window = 300)
   emaSlow =     EMAIndicator(close = inputData, window = 200)
   emaMedium =   EMAIndicator(close = inputData, window = 100)
   emaFast =     EMAIndicator(close = inputData, window = 50)
   rsi1 = RSIIndicator(close = inputData, window = 50)
   rsi2 = RSIIndicator(close = inputData, window = 100)
   rsi3 = RSIIndicator(close = inputData, window = 200)

   emaVerySlow = np.array(emaVerySlow.ema_indicator())
   emaSlow = np.array(emaSlow.ema_indicator())
   emaMedium = np.array(emaMedium.ema_indicator())
   emaFast = np.array(emaFast.ema_indicator())
   rsi1 = np.array(rsi1.rsi())
   rsi2 = np.array(rsi2.rsi())
   rsi3 = np.array(rsi3.rsi())

   data.insert(1, "fast", signal._emafast)
   data.insert(1, "macd", signal.macd())
   data.insert(1, "diff", signal.macd_diff())
   data.insert(1, "signal", signal.macd_signal())
   data.insert(1, 'emaVerySlow', emaVerySlow)
   data.insert(1, 'emaVerySlow-1', np.roll(emaVerySlow, -1))
   data.insert(1, 'emaVerySlow-2', np.roll(emaVerySlow, -2))
   data.insert(1, 'emaSlow', emaSlow)
   data.insert(1, 'emaSlow-1', np.roll(emaSlow, -1))
   data.insert(1, 'emaSlow-2', np.roll(emaSlow, -2))
   data.insert(1, 'emaMedium', emaMedium)
   data.insert(1, 'emaMedium-1', np.roll(emaMedium, -1))
   data.insert(1, 'emaMedium-2', np.roll(emaMedium, -2))
   data.insert(1, 'emaFast', emaFast)
   data.insert(1, 'emaFast-1', np.roll(emaFast, -1))
   data.insert(1, 'emaFast-2', np.roll(emaFast, -2))
   data.insert(1, 'rsi1', rsi1)
   data.insert(1, 'rsi2', rsi2)
   data.insert(1, 'rsi3', rsi3)
   #print(data.head)

   data = data.dropna()
   #print(data)

   print("data completo")


   return data, featuresName

def addOnlySmaToDatabase(data):
   inputData = data.iloc[:,1]

   featureNames = []

   start = 1
   stop = 1000
   step = 20
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

def addOnlyEmaToDatabase(data):
   inputData = data.iloc[:,1]

   featureNames = []

   start = 1
   stop = 3000
   step = 20
   for i in range(start, stop, step):
      ema = EMAIndicator(close = inputData, window = i)
      ema = np.array(ema.ema_indicator())
      originalEma = ema
      #name = "ema_{0}".format(i)

      for delay in range(0, 50, 10):
         name = "ema_{0}_{1}".format(i, delay)
         ema = np.roll(originalEma, delay)
         
         #il compilatore si lamenta che questo è lento
         #data.insert(1, name, ema)
         featureNames.append(name)

         #più veloceeeeee!!
         df = pd.DataFrame(ema, columns = [name])
         data = pd.concat([data, df], axis = 1, names = [list(data.columns), name])
      
   return data, featureNames

def addOnlyRsiToDatabase(data):
   inputData = data.iloc[:,1]

   featureNames = []

   start = 1
   stop = 1000
   step = 20
   for i in range(start, stop, step):
      rsi = RSIIndicator(close = inputData, window = i)
      rsi = np.array(rsi.rsi())
      name = "rsi_{0}".format(i)
      
      #il compilatore si lamenta che questo è lento
      #data.insert(1, name, rsi)
      featureNames.append(name)      
      
      #più veloceeeeee!!
      df = pd.DataFrame(rsi, columns = [name])
      data = pd.concat([data, df], axis = 1, names = [list(data.columns), name])
      
   return data, featureNames

def addOnlyAwesomeOscillatorToDatabase(data):
   inputData = data.iloc[:,1]

   high = data.iloc[:,2]
   low = data.iloc[:,3]

   featureNames = []

   start = 1
   stop = 1000
   step = 20
   for i in range(start, stop, step):
      awesome = AwesomeOscillatorIndicator(high, low, window1 = 5, window2 = 34)
      awesome = np.array(awesome.awesome_oscillator())
      name = "awesome_{0}".format(i)
      
      #il compilatore si lamenta che questo è lento
      #data.insert(1, name, rsi)
      featureNames.append(name)      
      
      #più veloceeeeee!!
      df = pd.DataFrame(awesome, columns = [name])
      data = pd.concat([data, df], axis = 1, names = [list(data.columns), name])
      
   return data, featureNames

def addOnlyKAMAToDatabase(data):
   inputData = data.iloc[:,1]

   high = data.iloc[:,2]
   low = data.iloc[:,3]

   featureNames = []

   start = 1
   stop = 1000
   step = 20
   for i in range(start, stop, step):
      awesome = KAMAIndicator(inputData)
      awesome = np.array(awesome)
      name = "awesome_{0}".format(i)
      
      #il compilatore si lamenta che questo è lento
      #data.insert(1, name, rsi)
      featureNames.append(name)      
      
      #più veloceeeeee!!
      df = pd.DataFrame(awesome, columns = [name])
      data = pd.concat([data, df], axis = 1, names = [list(data.columns), name])
      
   return data, featureNames


def splitDataIntoTrainAndTestSetGivenCertainPercentage(X, y, percentage):
   #(totalNumberOfEntries, uselessVar) = data.shape
   #totalNumberOfEntries = 1000
   (totalNumberOfEntries, uselessVar) = X.shape
   trainSize = int(totalNumberOfEntries * float(percentage))
   testSize = totalNumberOfEntries - trainSize

   x_train = X.iloc[0:trainSize, :]
   y_train = y.iloc[0:trainSize]
   x_test = X.iloc[trainSize:totalNumberOfEntries, :]
   y_test = y.iloc[trainSize:totalNumberOfEntries]
   print("train entries: {0}".format(x_train.shape))
   print("train labels: {0}".format(y_train.shape))
   print("test entries: {0}".format(x_test.shape))
   print("test labels: {0}".format(y_test.shape))

   return (x_train, y_train, x_test, y_test)

def addFeatureToDatabase(data):
   #data, featuresName = addFeatureToDatabase(data)
   
   data, f1 = addOnlyEmaToDatabase(data)
   #data, f2 = addOnlyRsiToDatabase(data)
   #data, f3 = addOnlySmaToDatabase(data)
   #data, f4 = addOnlyAwesomeOscillatorToDatabase(data)
   data = data.dropna()
   print(data)
   print("data completo")
   featuresName = f1
   #featuresName.extend(f2)
   #featuresName.extend(f3)

   return data, featuresName

def trainWithCrossValidation(train_features, train_labels):
   from sklearn.model_selection import RandomizedSearchCV
   
   n_estimators = [3, 6, 10, 30, 60, 100, 300, 600, 1000, 3000, 6000, 10000]
   max_depth = [3, 6, 10, 30, 60, 100]
   
   # Create the random grid
   random_grid = {'n_estimators': n_estimators,
   'max_depth': max_depth}

   rf = RandomForestClassifier()
   rf_random = RandomizedSearchCV(estimator = rf, n_iter = int(len(n_estimators))*int(len(max_depth)), param_distributions = random_grid, cv = 10, verbose = 4, random_state = 42, n_jobs = 4)
   rf_random.fit(train_features, train_labels)

   print(rf_random.best_params_)

### varie

def printCountOfEntryForEachClass(data, numberOfEntry):
   print("conteggio classi")
   numberOf0 = 0
   numberOf1 = 0
   numberOfNo1 = 0
   '''
   for i in range(numberOfEntry):
      if(data.iloc[i]["class"] == 0):
         numberOf0 = numberOf0 + 1
      if(data.iloc[i]["class"] == 1):
         numberOf1 = numberOf1 + 1
      if(data.iloc[i]["class"] == -1):
         numberOfNo1 = numberOfNo1 + 1
   '''
   (numberOf0, useless) = data[data['class'] == 0].shape
   (numberOf1, useless) = data[data['class'] == 1].shape
   (numberOfNo1, useless) = data[data['class'] == -1].shape

   print("class 0 = {0}".format(numberOf0))
   print("class 1 = {0}".format(numberOf1))
   print("class -1= {0}".format(numberOfNo1))

   #plt.bar(['0', '+1', '-1'], [numberOf0, numberOf1, numberOfNo1])
   #plt.show()

def findBestFeaturesInGreedyWay(data):
   numberOfFeaturesScanned = 0
   numberOfFeaturesCurrentlyUsed = 0
   featuresName = list(data.columns)
   currentFeaturesList = []

   for i in range(1, len(featuresName), 1):
      currentFeaturesList.append(featuresName[i+6])
      numberOfFeaturesCurrentlyUsed = numberOfFeaturesCurrentlyUsed + int(1)

      X = data.loc[:, currentFeaturesList]
      y = data[:]["class"]

      #X = X.iloc[0:10000]
      #y = y.iloc[0:10000]
      (x_train, y_train, x_test, y_test) = splitDataIntoTrainAndTestSetGivenCertainPercentage(X, y, 0.9)
      
      now = datetime.now().strftime("%H:%M:%S")
      print("train start at {0}".format(now))
      
      classifier = RandomForestClassifier(max_depth = 4, n_estimators = 800, n_jobs= -1 )
      classifier = classifier.fit(x_train, y_train)

      now = datetime.now().strftime("%H:%M:%S")
      print("train end at {0}".format(now))
      
      importances = classifier.feature_importances_

      for j in range(len(importances)-1, 0, -1):
         minimumThreshold = float(1 / j / 10)
         if(importances[j] < minimumThreshold):
            del currentFeaturesList[j]
            numberOfFeaturesCurrentlyUsed = numberOfFeaturesCurrentlyUsed - int(1)
        
def saveModel(classifier):
   joblib.dump(classifier, BASE_PATH + "random_forest.joblib")

def loadModel():
   return joblib.load(BASE_PATH + "random_forest.joblib")

def finndMostImportantFeature(x_train, y_train, featuresName):
   weights = []
   weights.append(featuresName)
   for i in range(1, 20, 1):
      now = datetime.now().strftime("%H:%M:%S")
      print("train start at {0}".format(now))
      
      classifier = RandomForestClassifier(max_depth = i, n_estimators = 1600, n_jobs= -1, min_samples_leaf = 400)
      classifier = classifier.fit(x_train, y_train)

      now = datetime.now().strftime("%H:%M:%S")
      print("train end at {0}".format(now))
            
      importances = classifier.feature_importances_
      weights.append(importances)

   f = open("pandas/weights.txt", 'w')
   for line in weights:
      #f.write(str(line) )
      for entry in line:
         f.write(str(entry) + ',')
      f.write('\n')
   f.close()
   
   
### plot

def plotFeatureImportance(classifier, x_test, y_test, featuresName):
   #https://scikit-learn.org/stable/auto_examples/ensemble/plot_forest_importances.html
   importances = classifier.feature_importances_
   std = np.std([tree.feature_importances_ for tree in classifier.estimators_], axis=0)
   plt.bar(featuresName, std)
   #plt.bar(list(range(0, len(std))) ,std)
   plt.show()

   result = permutation_importance(classifier, x_test, y_test, n_repeats=10, random_state=42, n_jobs=2)
   plt.bar(featuresName, result.importances_std)
   #plt.bar(list(range(0, len(std))) ,result.importances_std)
   plt.show()

def plotProbabilityOfDetectionAsFunctionOfThreshold(y_real, y_pred, probabilities):
   '''
   dio cane, è chiaro che se alzo la threshold della probabilità sono più sicuro dei dati che ho calcolato,
   ovvio che in questo modo i "true positive" dovrebbero aumentare e di conseguenza anche la 
   "precision", ma vista la curva precision/recall che ho e che è una merda questo non accade
   '''
   x_axis = []
   y_axis = []
   total = []
   '''
   for intPercentage in range(50, 90, 1):
      percentage = float(intPercentage / 100)
      x_axis.append(str(percentage))
      numberOfPredicted1 = 0
      numberOfReal1 = 0
      for i in range(len(y_real)):
         if(probabilities[i] > percentage):
            if(int(y_pred[i]) == 1):
               numberOfPredicted1 = numberOfPredicted1 + 1
            if(int(y_real[i]) == 1):
               numberOfReal1 = numberOfReal1 + 1
      total.append(numberOfPredicted1)
      if(numberOfPredicted1 == 0):
         y_axis.append(0)
      else:
         y_axis.append(float(numberOfPredicted1))
   '''
   y_real = np.array(y_real)
   y_pred = np.array(y_pred)
   
   for intPercentage in range(50, 70, 1):
      percentage = float(intPercentage / 100)
      x_axis.append(str(percentage))
      localPred = []
      numberOfPredicted1 = 0
      numberOfReal1 = 0
      for i in range(len(y_real)):
         if(probabilities[i] > percentage):
            localPred.append(1)
         else:
            localPred.append(-1)
      localPred = np.array(localPred)
      retval = sklearn.metrics.confusion_matrix(y_real, localPred)
      tn = retval[0][0]
      fn = retval[0][1]
      fp = retval[1][0]
      tp = retval[1][1]
      
      quantity = 0
      for i in range(len(y_real)):
         if (probabilities[i] >= percentage):  
            quantity = quantity + int(1)

      #y_axis.append(tp/(tp+fp))
      if(quantity != 0):
         y_axis.append(tp/quantity)
      else:
         y_axis.append(0)

   #plt.bar(x_axis, y_axis)
   #plt.show()

   fig, ax = plt.subplots()
   bar_container = ax.bar(x_axis, y_axis)
   #ax.set(ylabel='pints sold', title='Gelato sales by flavor', ylim=(0, 8000))
   #ax.bar_label(bar_container, labels=['±%.2f' % e for e in total])
   plt.show()

def plotTrainAndTestError(x_train, y_train, x_test, y_test):
   trainError = []
   testError = []
   plt.ion()
   plt.show()
   for i in range(1, 10, 1):
      classifier = RandomForestClassifier(max_depth = i, n_estimators = 200, n_jobs = -1)
      classifier = classifier.fit(x_train, y_train)
      trainError.append(1 - classifier.score(x_train, y_train))
      testError.append(1 - classifier.score(x_test, y_test))
   plt.plot(trainError, 'k')
   plt.plot(testError, 'y')
   plt.legend(['train error', 'test error'])
   plt.draw()
   plt.pause(0.5)
   
def plotTree(classifier, featuresName):
   fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi=800)
   tree.plot_tree(classifier.estimators_[0], feature_names = featuresName, class_names = ['nothing', 'buy'] );
   fig.savefig('rf_individualtree.png')

   tree.plot_tree(classifier.estimators_[0])
   plt.show()





def main():
   #http://www.histdata.com/download-free-forex-historical-data/?/ascii/1-minute-bar-quotes/eurusd/2022

   #data = pd.read_csv("pandas/DAT_ASCII_EURUSD_M1_2022_gennaio.csv")
   #data = pd.read_csv(BASE_PATH + FILE_1M_ALL2022_ORIGNAL)
   #formatDatabase(data)
   #formatDatabaseWritingLinesOneByOne(data)

   #data = pd.read_csv("pandas/DAT_ASCII_EURUSD_M1_2022_gennaio_class.csv")
   data = pd.read_csv(BASE_PATH + FILE_1M_ALL2022_WINDOWS_100)#FILE_1M_ALL2022_WITH_CLASS)
   (numberOfRows, numberOfColumns) = data.shape
   print("data set size = {0}".format(data.shape))
   
   printCountOfEntryForEachClass(data, numberOfRows)

   #for i in range(numberOfRows):
   #   if(data.iloc[i]['class'] == 0):
   #      data.at[i, 'class'] = -1

   #https://www.geeksforgeeks.org/how-to-replace-values-in-column-based-on-condition-in-pandas/
   #data['class'] = np.where(data['class'] == 0, -1, data['class'])

   #data = data[data['class'] != 0]
   #data = pd.DataFrame(data)
   #data = np.where( (data['class'] == 1) | (data['class'] == -1) )
   #data = data[ (data['class'] == 1) | (data['class'] == -1) ]

   printCountOfEntryForEachClass(data, numberOfRows)

   data, featuresName = addFeatureToDatabase(data)
      
   X = data.loc[:, featuresName]
   y = data[:]["class"]

   
   #X = X.iloc[0:53000]
   #y = y.iloc[0:53000]
   #trainWithCrossValidation(X, y)
   
   (x_train, y_train, x_test, y_test) = splitDataIntoTrainAndTestSetGivenCertainPercentage(X, y, 0.9)
   
   #non so perchè questa merda funziona, ma funziona!
   numberOf1 = len(np.where(y_test == 1)[0])
   numberOf0 = len(np.where(y_test == 0)[0])
   numberOfNo1 = len(np.where(y_test == -1)[0])
   print("test set has {0} -1, {1} 0 and {2} 1".format(numberOfNo1, numberOf0, numberOf1))

   #findBestFeaturesInGreedyWay(data)

   '''
   classifier = loadModel()
   y_pred1 = classifier.predict(x_test)
   probabilities = classifier.predict_proba(x_test)
   features.printMultipleMeasures(y_test, y_pred1, np.array(probabilities[:,1]))
   plotProbabilityOfDetectionAsFunctionOfThreshold(np.array(y_test), np.array(y_pred1), np.array(probabilities[:,1]))
   '''

   now = datetime.now().strftime("%H:%M:%S")
   print("train start at {0}".format(now))
   
   #my_base_model = sklearn.tree.DecisionTreeClassifier(max_depth = 1)
   #classifier = AdaBoostClassifier(estimator = my_base_model, n_estimators = 200)
   
   classifier = RandomForestClassifier(max_depth = 6, n_estimators = 20000, n_jobs = 2 )
   #classifier = RandomForestClassifier(max_depth = 10, n_estimators = 200)
   classifier = classifier.fit(x_train, y_train)

   now = datetime.now().strftime("%H:%M:%S")
   print("train end at {0}".format(now))
   
   y_pred1 = classifier.predict(x_test)
   probabilities = classifier.predict_proba(x_test)

   #saveModel(classifier)

   features.printMultipleMeasures(y_test, y_pred1, np.array(probabilities[:,1]))
   plotProbabilityOfDetectionAsFunctionOfThreshold(y_test, y_pred1, np.array(probabilities[:,1]))

   plotFeatureImportance(classifier, x_test, y_test, featuresName)
   
   

if __name__ == "__main__":
   main()