
#questo serve per quando copio i dati nel vettore locale, visto che copio per riferimento se cambia l'oggetto dopo
#che ho chiamato la funzione cambia anche il dato salvato in locale
import copy

QUEUE_DIMENSION = 10

class queueForUnalignedTimeData:
   def __init__(self, timeDelta):
      self.lastDataAdded = 0
      self.dataQueue = []
      self.timeDelta = int(timeDelta)  #intrervalli in [0, delta], [delta, 2*delta], ... o più in generale [a*delta, (a+1)*delta]

   def addNewData(self, data):
      newData = copy.deepcopy(data)

      if(self.lastDataAdded == 0):
         self.lastDataAdded = newData
      else:
         if(newData["time"]["minute"] - self.lastDataAdded["time"]["minute"] > 2*self.timeDelta):  #è passato più del doppio del tempo di intervallo, devo aggiungere almeno un dato "fittizio"
            while(newData["time"]["minute"] - self.lastDataAdded["time"]["minute"] >= self.timeDelta):
               
               self.lastDataAdded["time"]["minute"] = self.findAllignedDataTimeLastData()
               self.lastDataAdded["time"]["second"] = int(0)
               self.dataQueue.append(copy.deepcopy(self.lastDataAdded))
               
         if(self.lastDataAdded["time"]["minute"] != newData["time"]["minute"] and
            self.lastDataAdded["time"]["minute"] < self.findAllignedDataTimeLastData() and
            newData["time"]["minute"] >= self.findAllignedDataTimeLastData() ):
            
            self.lastDataAdded["time"]["minute"] = self.findAllignedDataTimeLastData()
            self.lastDataAdded["time"]["second"] = int(0)
            self.dataQueue.append(self.lastDataAdded)
            
            self.lastDataAdded = newData
         else:
            self.lastDataAdded = newData

      #ogni tanto rimuovo elementi dalla coda per evitare che diventi troppo grande
      if(len(self.dataQueue) > QUEUE_DIMENSION):
         self.dataQueue.pop(0)

   def findAllignedDataTimeLastData(self):
      time = self.lastDataAdded["time"]["minute"]
      #if(time < self.timeDelta):
      #   return int(self.timeDelta)
      #elif(time < 2*self.timeDelta):
      #   return int(2*self.timeDelta)
      #elif(time < 3*self.timeDelta):
      #   return int(3*self.timeDelta)
      return int(time / self.timeDelta)*self.timeDelta + self.timeDelta
   
   


def test_addNewData():
   queue = queueForUnalignedTimeData(5)
   data = {
      "value": 0,
      "time" : {
         "minute": 4,
         "second": 50
      }
   }

   queue.addNewData(data)
   assert(queue.lastDataAdded["value"] == data["value"])
   assert(queue.lastDataAdded["time"]["minute"] == data["time"]["minute"])
   assert(queue.lastDataAdded["time"]["second"] == data["time"]["second"])

def test_addTwoDataBeforeTimeInterval_keepMostRecentValue():
   queue = queueForUnalignedTimeData(5)
   data = {
      "value": 0,
      "time" : {
         "minute": 4,
         "second": 50
      }
   }

   queue.addNewData(data)

   data["time"]["second"] = 55

   queue.addNewData(data)

   assert(queue.lastDataAdded["value"] == data["value"])
   assert(queue.lastDataAdded["time"]["minute"] == data["time"]["minute"])
   assert(queue.lastDataAdded["time"]["second"] == data["time"]["second"])

def test_addDataAfterTimeInterval_keepLastDataFromPreviousInterval():
   queue = queueForUnalignedTimeData(5)
   data = {
      "value": 0,
      "time" : {
         "minute": 4,
         "second": 50
      }
   }

   queue.addNewData(data)

   data["value"] = int(1)
   data["time"]["minute"] = int(5)
   data["time"]["second"] = int(7)

   queue.addNewData(data)

   assert(queue.dataQueue[0]["value"] == 0)
   assert(queue.dataQueue[0]["time"]["minute"] == data["time"]["minute"])
   assert(queue.dataQueue[0]["time"]["second"] == int(0))

def test_addMultipleDataAfterTimeInterval():
   queue = queueForUnalignedTimeData(5)
   data = {
      "value": 0,
      "time" : {
         "minute": 4,
         "second": 50
      }
   }

   queue.addNewData(data)

   data["value"] = int(1)
   data["time"]["minute"] = int(4)
   data["time"]["second"] = int(55)

   queue.addNewData(data)

   data["value"] = int(2)
   data["time"]["minute"] = int(5)
   data["time"]["second"] = int(1)

   queue.addNewData(data)

   assert(queue.dataQueue[0]["value"] == int(1))
   assert(queue.dataQueue[0]["time"]["minute"] == int(5))
   assert(queue.dataQueue[0]["time"]["second"] == int(0))

def test_addDataInDifferentTimeInterval():
   queue = queueForUnalignedTimeData(5)
   data = {
      "value": 0,
      "time" : {
         "minute": 4,
         "second": 50
      }
   }

   queue.addNewData(data)

   data["value"] = int(1)
   data["time"]["minute"] = int(5)
   data["time"]["second"] = int(55)

   queue.addNewData(data)

   data["value"] = int(2)
   data["time"]["minute"] = int(7)
   data["time"]["second"] = int(1)

   queue.addNewData(data)

   data["value"] = int(3)
   data["time"]["minute"] = int(11)
   data["time"]["second"] = int(8)

   queue.addNewData(data)

   assert(queue.dataQueue[0]["value"] == int(0))
   assert(queue.dataQueue[0]["time"]["minute"] == int(5))
   assert(queue.dataQueue[0]["time"]["second"] == int(0))

   assert(queue.dataQueue[1]["value"] == int(2))
   assert(queue.dataQueue[1]["time"]["minute"] == int(10))
   assert(queue.dataQueue[1]["time"]["second"] == int(0))

def test_addDataWithHugeTimeGapInBetween_fillMissingDataInTheArray():
   queue = queueForUnalignedTimeData(5)
   data = {
      "value": 1,
      "time" : {
         "minute": 4,
         "second": 50
      }
   }

   queue.addNewData(data)

   data["value"] = int(8)
   data["time"]["minute"] = int(15)
   data["time"]["second"] = int(55)

   queue.addNewData(data)

   assert(queue.dataQueue[0]["value"] == int(1))
   assert(queue.dataQueue[0]["time"]["minute"] == int(5))
   assert(queue.dataQueue[0]["time"]["second"] == int(0))

   assert(queue.dataQueue[1]["value"] == int(1))
   assert(queue.dataQueue[1]["time"]["minute"] == int(10))
   assert(queue.dataQueue[1]["time"]["second"] == int(0))

   assert(queue.dataQueue[2]["value"] == int(1))
   assert(queue.dataQueue[2]["time"]["minute"] == int(15))
   assert(queue.dataQueue[2]["time"]["second"] == int(0))



if __name__ == "__main__":
   test_addNewData()
   test_addTwoDataBeforeTimeInterval_keepMostRecentValue()
   test_addDataAfterTimeInterval_keepLastDataFromPreviousInterval()
   test_addMultipleDataAfterTimeInterval()
   test_addDataInDifferentTimeInterval()
   test_addDataWithHugeTimeGapInBetween_fillMissingDataInTheArray()

   print("end")