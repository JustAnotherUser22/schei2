


def solution(data, n):
   
   dataLength = len(data)
   result = data.copy()

   if(dataLength > 100):
      return
   
   if(n < 0):
      return

   for i in range(dataLength):
      currentElement = data[i]
      numberOfOccurrence = 1

      for j in range(i + 1, dataLength):
         if currentElement == data[j]:
            numberOfOccurrence = numberOfOccurrence + 1

      if(numberOfOccurrence > n):
         for k in range(numberOfOccurrence):
            if(currentElement in result):
               result.remove(currentElement)
         
   #print(result)
   return result

def solution2(data, n):
   dataLength = len(data)
   
   if(dataLength > 100):
      return
   
   if(n < 0):
      return

   listOfIndexToRemove = []
   for i in range(dataLength):
      listOfIndexToRemove.append(False)

   for i in range(dataLength):
      currentElement = data[i]
      numberOfOccurrence = 1

      for j in range(i + 1, dataLength):
         if (currentElement == data[j]):
            numberOfOccurrence = numberOfOccurrence + 1

      if(numberOfOccurrence > n):
         for k in range(dataLength):
            if(data[k] == currentElement):
               if(listOfIndexToRemove[k] == False):
                  listOfIndexToRemove[k] = True

   for i in range(len(listOfIndexToRemove) - 1, -1, -1):
      if(listOfIndexToRemove[i] == True):
         data.pop(i)
         
   print(data)
   return data



def test1():
   result = solution2([1, 2, 3], 0)
   assert(result == [])

   
def test2():
   result = solution2([1, 2, 2, 3, 3, 3, 4, 5, 5], 1)
   assert(result == [1, 4])

   
if __name__ == "__main__":
   test1()
   test2()
   