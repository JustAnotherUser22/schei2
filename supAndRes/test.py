from supAndRes import *

from datetime import timezone
import datetime

def DetectMax_when_thereIsMax_then_detectIt():
   value = DetectMax(1, 2, 3)
   assert(value == False)

   value = DetectMax(3, 2, 1)
   assert(value == False)

   value = DetectMax(1, 2, 1.5)
   assert(value == True)

def DetectMin_when_thereIsMin_then_detectIt():
   value = DetectMin(1, 2, 3)
   assert(value == False)

   value = DetectMin(3, 2, 1)
   assert(value == False)

   value = DetectMin(3, 2, 4)
   assert(value == True)

def AddValueToQueue_when_addValue_then_doIt():
   queue = []
   AddValueToQueue(queue, 1)
   AddValueToQueue(queue, 2)
   AddValueToQueue(queue, 3)

   assert(queue[0] == 1)
   assert(queue[1] == 2)
   assert(queue[2] == 3)

def AddValueToQueue_when_addToManyValues_then_keepTheLastOnes():
   queue = []
   AddValueToQueue(queue, 1)
   AddValueToQueue(queue, 2)
   AddValueToQueue(queue, 3)
   AddValueToQueue(queue, 4)
   AddValueToQueue(queue, 5)
   AddValueToQueue(queue, 6)

   assert(queue[0] == 4)
   assert(queue[1] == 5)
   assert(queue[2] == 6)

def PrintFakeLine():
   first = Point(1, 2)
   second = Point(4, 4)
   third = Point(7, 5)
   printLineFromFirstPointToThirdWithSlopeDueToSecondPoint(first, second, third, "dashed")
   plt.plot(first.x, first.y, 'bo')
   plt.plot(second.x, second.y, 'bo')
   plt.plot(third.x, third.y, 'bo')
   plt.show()

def ConvertTimeToUTC():
   
   #https://www.geeksforgeeks.org/get-utc-timestamp-in-python/
   
   dt = datetime.datetime(1999, 12, 12, 12, 12, 12, 342380) 
   print(dt)
   utc_time = dt.replace(tzinfo = timezone.utc)
   utc_timestamp = utc_time.timestamp()
   print(utc_timestamp)


def Test():
   DetectMax_when_thereIsMax_then_detectIt()
   DetectMin_when_thereIsMin_then_detectIt()
   AddValueToQueue_when_addValue_then_doIt()
   AddValueToQueue_when_addToManyValues_then_keepTheLastOnes()
   PrintFakeLine()
   ConvertTimeToUTC()

   print("ok")


if __name__ == "__main__":
   Test()