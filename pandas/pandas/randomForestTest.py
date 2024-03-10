import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.inspection import DecisionBoundaryDisplay


def main():

   data = pd.DataFrame({'f1':    [1, 1, 0, 0, 0, 0], 
                        'f2':    [0, 0, 1, 1, 0, 0],
                        'f3':    [0, 0, 0, 0, 1, 1],
                        'class': [1, 1, 2, 2, 3, 3]})

   model = train(data)
   #saveOrPlotTree(data, model)
   
   plotboundaries(data)



def train(data):
   print(data)
   print("data shape is {0}".format(data.shape) )

   X = data.loc[: , ['f1', 'f2', 'f3']]
   #y = data.iloc[:, 3]
   y = data.loc[:, 'class']

   #print(X)
   print("input shape is {0}".format(X.shape))
   #print(y)
   print("output shape is {0}".format(y.shape))

   classifier = RandomForestClassifier(max_depth = 2)
   classifier = classifier.fit(X, y)

   #dato = X.iloc[[1]]
   #print(dato)

   dato = pd.DataFrame({'f1': [1], 
                        'f2': [0],
                        'f3': [0] })

   print(classifier.predict(dato))
   print(classifier.predict_proba(dato))

   return classifier



def saveOrPlotTree(data, randomForest):
   fn = list(data.columns)
   cn = list(['1', '2', '3'])

   fig, axes = plt.subplots(nrows = 1,ncols = 1,figsize = (4,4), dpi = 800)

   tree.plot_tree(randomForest.estimators_[0],
                  feature_names = fn, 
                  class_names = cn,
                  filled = True);
   fig.savefig('schei2/pandas/pandas/rf_individualtree.png')



def plotboundaries(data):
   
   X = data.loc[: , ['f1', 'f2'] ]
   y_train = data.loc[:, 'class']

   classifier = RandomForestClassifier(max_depth = 2)
   classifier = classifier.fit(X, y_train)
   
   disp = DecisionBoundaryDisplay.from_estimator(
      classifier, 
      X, 
      #response_method = "predict",
      #xlabel=iris.feature_names[0],
      #ylabel=iris.feature_names[1],
      #alpha = 0.5,
      )
   
   firstFeature = X.iloc[:, 0]
   secondFeature = X.iloc[:,1]
   y = data.loc[:, 'class']
   disp.ax_.scatter(firstFeature, secondFeature, c = y,
                    edgecolor="k",
                    cmap = plt.cm.coolwarm)

   plt.show()


if __name__ == "__main__":
   main()