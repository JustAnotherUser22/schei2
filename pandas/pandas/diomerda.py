from sklearn.metrics import confusion_matrix

real = [0, 0, 0, 1, 1]
pred = [0, 0, 0, 0 ,0]

print(confusion_matrix(real, pred))

'''
dalla pagina web 
https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
trovo che la matrice è nella forma

   true negative  | false positive
   -----------------------------
   false negative | true positive

'''