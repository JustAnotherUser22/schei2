import numpy as np
from supAndRes import *

#HIST_DATA_PATH = "C:/Users\Marco\Documents\python\supAndRes\EURUSD_M1_2022_02.csv"
HIST_DATA_PATH = "D:\script\supAndRes\EURUSD_M1_2022_02.csv"

DAY = 1
HOUR = 2
EVERYTIME = 3
FIVE_MINUTES = 4
THIRTY_MINUTES = 5
TWO_MINUTES = 6
TEN_MINUTES = 7

POSITION_YEAR =   0
POSITION_MONTH =  1
POSITION_DAY =    2
POSITION_HOUR =   3
POSITION_MINUTE = 4
POSITION_SECOND = 5
POSITION_OPEN =   6
POSITION_HIGH =   7
POSITION_LOW =    8
POSITION_CLOSE =  9

##############################
#  private methods
##############################

def getDataFromEntry(entry):
   year = entry[POSITION_YEAR]
   month = entry[POSITION_MONTH]
   day = entry[POSITION_DAY]
   hour = entry[POSITION_HOUR]
   minute = entry[POSITION_MINUTE]
   second = entry[POSITION_SECOND]

   return (year, month, day, hour, minute, second)

def HIST_IsDay(entry):
   (year, month, day, hour, minute, second) = getDataFromEntry(entry)

   if(hour == 0 and minute == 0 and second == 0):
      return True
   else:
      return False
   
def HIST_IsHour(entry):
   (year, month, day, hour, minute, second) = getDataFromEntry(entry)

   if(minute == 0 and second == 0):
      return True
   else:
      return False
  
   
def HIST_alwaysTrue(entry):
   return True

def HIST_IsCretainNumberOfMinute(entry, numberOfMinute):
   (year, month, day, hour, minute, second) = getDataFromEntry(entry)
   
   if(minute % numberOfMinute == 0 and second == 0):
      return True
   else:
      return False

 
def HIST_IsFiveMinutes(entry):
   return HIST_IsCretainNumberOfMinute(entry, 5)

def HIST_IsThirtyMinutes(entry):
   return HIST_IsCretainNumberOfMinute(entry, 30)
   
def HIST_IsTwoMinutes(entry):
   return HIST_IsCretainNumberOfMinute(entry, 2)

def HIST_IsTenMinutes(entry):
   return HIST_IsCretainNumberOfMinute(entry, 10)



def findCertainSequenceInGivenDataPoint(sequenceType, data):
   sequence = []
   
   start = 3
   stop = len(data)
   step = 1

   f = 0
   if(sequenceType == MAX):
      f = DetectMax
   elif (sequenceType == MIN):
      f = DetectMin

   for i in range(start, stop, step):
      if(f(data[i-2].y, data[i-1].y, data[i].y) == True):
         sequence.append(data[i-1])

   return sequence

##############################
#  public methods
##############################

def convertDateTimeToInteger(year, month, day, hour, minute, second):
   globalTime = int(second)
   globalTime += int(minute) * 60
   globalTime += int(hour) * 60 * 60
   globalTime += int(day) * 24 * 60 * 60

def load_HIST_Data():
   matrix = []

   f = open(HIST_DATA_PATH, 'r')
   lines = f.readlines()

   for i in range(len(lines)): 
      data = lines[i].split(";")
      time = data[0].split(" ")

      year = time[0][0:4]
      month = time[0][4:6]
      day = time[0][6:8]

      hour = time[1][0:2]
      minute = time[1][2:4]
      second = time[1][4:6]

      array = []
      array.append(int(year))
      array.append(int(month))
      array.append(int(day))
      array.append(int(hour))
      array.append(int(minute))
      array.append(int(second))
      array.append(float(data[1].replace('\'', '').replace(',','.')))   #open
      array.append(float(data[2].replace('\'', '').replace(',','.')))   #high
      array.append(float(data[3].replace('\'', '').replace(',','.')))   #low
      array.append(float(data[4].replace('\'', '')))                    #close
      matrix.append(array)

   matrix = np.array(matrix)

   return matrix

def HIST_findDataEveryTimeInterval(data, timeInterval):
   array = []
   
   condition = 0

   if(timeInterval == DAY):
      condition = HIST_IsDay
   elif(timeInterval == HOUR):
      condition = HIST_IsHour
   elif(timeInterval == EVERYTIME):
      condition = HIST_alwaysTrue
   elif(timeInterval == FIVE_MINUTES):
      condition = HIST_IsFiveMinutes
   elif(timeInterval == THIRTY_MINUTES):
      condition = HIST_IsThirtyMinutes
   elif(timeInterval == TWO_MINUTES):
      condition = HIST_IsTwoMinutes
   elif(timeInterval == TEN_MINUTES):
      condition = HIST_IsTenMinutes

   for i in range(len(data)):
      entry = data[i]
      if(condition(entry) == True):
         #array.append(Point(i, entry[4]))
         array.append(Point(i, entry[9]))

   return array

def HIST_findMinInPointSequence(Pointsequence):
   return findCertainSequenceInGivenDataPoint(MIN, Pointsequence)

def HIST_findMaxInPointSequence(Pointsequence):
   return findCertainSequenceInGivenDataPoint(MAX, Pointsequence)






if __name__ == "__main__":
   pass