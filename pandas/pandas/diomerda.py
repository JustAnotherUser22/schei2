from sklearn.metrics import confusion_matrix

real = [0, 0, 0, 1, 1]
pred = [0, 0, 0, 0 ,0]

print(confusion_matrix(real, pred))