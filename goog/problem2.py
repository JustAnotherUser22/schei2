'''
def sumOfAllNumber(L):
   sum = 0
   for i in range(len(L)):
      sum = sum + L[i]
   return sum
'''

'''
def generateAllPossibleListWithoutOneItem(L):
   allList = []
   localList = L.copy()
   
   for i in range(0, len(L), 1):
      localList.pop(i)
      allList.append(localList.copy())
      localList = L.copy()
   
   return allList
'''

def generateNumberFromList(L):
   number = ''
   for i in range(len(L)):
      number = number + str(L[i])

   number = int(number)
   return number



def generateAllPossibleList(L):
   allList = []
   
   listLength = len(L)

   for number in range(1, 2**listLength, 1):
      localList = []
      tmp = bin(number)
      
      res = [x for x in str(tmp)]
      res.pop(0)
      res.pop(0)

      while(len(res) < listLength):
         res.insert(0, 0)

      for i in range(listLength - 1, -1, -1):
         if (res[i] == '1'):
            localList.insert(0, L[i])
      
      allList.append(localList.copy())

   return allList


def solution(l):
   
   l.sort(reverse = True)
   localList = l.copy()
   currentMaxValue = 0

   allLists = generateAllPossibleList(localList)

   for L in allLists:
      n = generateNumberFromList(L)
      if(n % 3 == 0):
         if(n > currentMaxValue):
            currentMaxValue = n

   return currentMaxValue

def localTest():
   #assert(sumOfAllNumber([1, 2, 3]) == 6)
   assert(generateNumberFromList([1, 2, 3]) == 123)
   #assert(generateAllPossibleListWithoutOneItem([1, 2, 3]) == [ [2, 3], [1, 3], [1, 2] ])
   #assert(generateAllPossibleList([]) == [])
   assert(generateAllPossibleList([1, 2, 3]) == [])

   print('ok')

def main():
   assert(solution([3, 1, 4, 1]) == 4311)
   assert(solution([3, 1, 4, 1, 5, 9]) == 94311)
   print("end")


if __name__ == "__main__":
   main()