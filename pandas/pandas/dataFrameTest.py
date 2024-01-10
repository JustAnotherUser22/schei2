import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def createDatabaseAndShowit():
   data = pd.DataFrame({'Yes': [50, 21], 'No': [131, 2]})
   print("---data e shape")
   print(data)
   print(data.shape)
   print()

def changeValueInDatabase():
   data = pd.DataFrame({'Yes': [50, 21], 'No': [131, 2]})

   #cambia il valore in posizione (1,1)
   data.iloc[1][1] = 66
   data.iloc[1]['Yes'] = 11
   data.loc[1][1] = 666
   data.loc[1]['Yes'] = 11
   print("---data dopo aver cammbiato una entry")
   print(data)
   print()

def printSingleEntry():
   data = pd.DataFrame({'Yes': [50, 21], 'No': [131, 2]})

   #dio cane a chi ha inventato questo modo di printare
   print("---entry singola (con loc)")
   print(data.loc[1])
   print()

   print("---ancora entry singola (con loc)")
   print(data.loc[[1]])
   print() 

   print("---entry singola con (iloc)")
   print(data.iloc[1])
   print() 

   print("---ancora entry singola (con iloc)")
   print(data.iloc[[1]])
   print() 

   print("---vari modi di accedere a un dato")
   print(data.loc[1].No)
   print(data.loc[1]["No"])
   print(data.loc[1][1])
   print()

   print("---")
   print(data.iloc[[1]].to_string(header = False, index = False))

def addColumn():
   data = pd.DataFrame({'Yes': [50, 21], 'No': [131, 2]})
   print("---aggiungo una colonna")
   data.insert(1, "maybe", [0, 1])
   print(data)
   print()

   print("---questa è una colonna")
   #porco dio questa è una colonna invece...
   porcodio = data.loc[:, "Yes"]
   porcodio = data.iloc[:, 1] 
   print(porcodio)
   print()

def removeNaNEntries():
   data = pd.DataFrame({'Yes': [np.nan, 50, 21], 'No': [131, 2, np.nan]})
   print(data)
   #data = data[pd.notnull(data.Yes)]
   #data = data[pd.notnull(data.No)]
   data = data[pd.notna(data)]
   print(data)



if __name__ == "__main__":
   #createDatabaseAndShowit()
   changeValueInDatabase()
   #printSingleEntry()
   #addColumn()
   #removeNaNEntries()