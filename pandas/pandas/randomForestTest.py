import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from ta.trend import MACD
from sklearn.metrics import confusion_matrix

data = pd.DataFrame({'f1':    [1, 1, 0, 0, 0, 0], 
                     'f2':    [0, 0, 1, 1, 0, 0],
                     'f3':    [0, 0, 0, 0, 1, 1],
                     'class': [1, 1, 2, 2, 3, 3]})

print(data)
print(data.shape)

X = data.loc[: , ['f1', 'f2', 'f3']]
y = data.iloc[:, 3]
print(X)
print(X.shape)
print(y)
print(y.shape)

classifier = RandomForestClassifier(max_depth = 2)
classifier = classifier.fit(X, y)

dato = X.iloc[[1]]
print(dato)

dato = pd.DataFrame({'f1': [1], 
                     'f2': [1],
                     'f3': [1] })

print(classifier.predict(dato))
print(classifier.predict_proba(dato))