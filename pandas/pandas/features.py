from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import PrecisionRecallDisplay
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import precision_recall_curve
import sklearn.metrics
import matplotlib.pyplot as plt 

def printConfusionMatrix(y_real, y_pred):
   print(confusion_matrix(y_real, y_pred))
   values = confusion_matrix(y_real, y_pred)
   print("           pred 0         pred 1")
   print("real 0        {0}            {1}".format(values[0][0], values[0][1]))
   print("real 1        {0}           {1}".format(values[1][0], values[1][1]))

   sklearn.metrics.ConfusionMatrixDisplay.from_predictions(y_real, y_pred)

def plotROCCurve(y, y_pred):
   #https://scikit-learn.org/stable/modules/generated/sklearn.metrics.RocCurveDisplay.html#sklearn.metrics.RocCurveDisplay.from_estimator

   #fpr, tpr, thresholds = sklearn.metrics.roc_curve(y_true = y, y_score = y_pred)
   #roc_auc = sklearn.metrics.auc(fpr, tpr)
   #display = sklearn.metrics.RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name='example estimator')
   #display.plot()
   #plt.show()

   RocCurveDisplay.from_predictions(y, y_pred, plot_chance_level = True)
   plt.show()

def plotPrecisionAndRecallWithEstimator(classifier, x_test, y_test):
   display = PrecisionRecallDisplay.from_estimator(classifier, x_test, y_test, name = "LinearSVC", plot_chance_level = True)
   display.ax_.set_title("2-class Precision-Recall curve")   
   plt.show()

def plotPrecisionAndRecallWithPredictions(y_true, y_pred):
   #display = PrecisionRecallDisplay.from_estimator(classifier, x_test, y_test, name = "LinearSVC", plot_chance_level = True)
   display = PrecisionRecallDisplay.from_predictions(y_true = y_true, y_pred = y_pred, name = "LinearSVC", plot_chance_level = True)
   display.ax_.set_title("2-class Precision-Recall curve")   
   plt.show()

def plotPrecisionRecallAndThresholdWithoutWrapper(y_test, probabilities):
   precision, recall, thresholds = precision_recall_curve(y_test, probabilities)
   plt.plot(precision, label = 'precision')
   plt.plot(recall, 'k--', label = 'recall')
   plt.plot(thresholds, 'k:', label = 'threshold')
   plt.legend()
   plt.show()
   
   #plt.plot(recall, precision)   #così ottengo lo stesso grafico generato con l'altra funzione
   #plt.show()

def plotAccuracyAsFunctionOfThreshold(y_test, y_pred, probabilities):
   precision, recall, thresholds = precision_recall_curve(y_test, probabilities)
   
   accuracyValues = []
   cnt = 0

   for tresholdValue in thresholds:
      
      predictionWithGivenThreshold = []
      
      for i in range(len(probabilities)):
         if(probabilities[i] > tresholdValue):
            predictionWithGivenThreshold.append(1)
         else:
            predictionWithGivenThreshold.append(0)

      accuracy = accuracy_score(y_test, predictionWithGivenThreshold)
      accuracyValues.append(accuracy)

   y = accuracyValues
   x = thresholds
   plt.plot(x, y)
   plt.xlabel('threshold')
   plt.ylabel('accuracy')
   plt.suptitle('accuracy vs threshold graph')
   plt.show()

def plotPrecisionRecallAsFunctionOfThreshold(y_test, probabilities):
   precision, recall, thresholds = precision_recall_curve(y_test, probabilities)

   plt.plot(thresholds, precision[:-1], 'k--', label = 'precision')
   plt.plot(thresholds, recall[:-1], 'k:', label = 'recall')
   plt.legend()
   plt.show()


def printMultipleMeasures(y_real, y_pred, probabilities):
   """
   docstring

   Parameters
   ----------
   y_real : vettore contenente le classi reali

   y_real : vettore contenente le classi predette dal programma

   probabilities : vettore contenente la  probabilità che l'entry corrispondente appartenga alla classe '1'
   """

   f1 = f1_score(y_real, y_pred)
   print("f1 score: {0}".format(f1))

   accuracy = accuracy_score(y_real, y_pred)
   print("accuracy score: {0}".format(accuracy))

   printConfusionMatrix(y_real, y_pred)

   plotROCCurve(y_real, y_pred)

   plotPrecisionAndRecallWithPredictions(y_real, probabilities)

   plotPrecisionRecallAndThresholdWithoutWrapper(y_real, probabilities)

   plotPrecisionRecallAsFunctionOfThreshold(y_real, probabilities)

   #plotAccuracyAsFunctionOfThreshold(y_real, y_pred, probabilities)

