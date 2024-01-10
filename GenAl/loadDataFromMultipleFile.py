
import datetime
from datetime import timedelta
from fileinput import filename

FILE_NAME = "D:/script/GenAl/files/file_{0}.csv"

############################
#  classi
############################

class FileManager:
   def __init__(self, fileName, n):
      self.currentIndex = 0
      self.currentFile = 0
      #self.currentLine = 0
      self.fine = False
      self.lastFile = n
      self.fileName = fileName
   
   def getNextLine(self):
      if(self.currentFile == 0):
         self.openNextFile()

      currentLine = self.currentFile.readline()

      if(currentLine == '' and self.currentIndex == self.lastFile):
         self.fine = True
         self.currentFile.close()
         return

      if(currentLine == ''):
         self.currentFile.close()
         self.currentIndex = self.currentIndex + 1
         self.openNextFile()
         currentLine = self.currentFile.readline()

      return currentLine.replace('\n', '')      

   def openNextFile(self):      
      path = self.fileName.format(self.currentIndex)
      self.currentFile = open(path)
      
class localData:
   def __init__(self):
      self.timeStamp = 0
      self.currentData = 0

############################
#  metodi statici
############################

def DeltaIsPositive(delta):
   if(delta.days > 0):
      return True
   if(delta.days == 0 and delta.seconds > 0):
      return True
   if(delta.days == 0 and delta.seconds == 0 and delta.microseconds > 0):
      return True
   return False


def generateTimeFromLine(line):
   parameters = line.split('\t')
   date = parameters[0].split('.')
   time = parameters[1].split(':')

   dataOnLine = datetime.datetime(year = int(date[0]),
                                  month = int(date[1]),
                                  day = int(date[2]),
                                  hour = int(time[0]),
                                  minute = int(time[1]),
                                  second = int(time[2].split('.')[0]),
                                  microsecond = int(time[2].split('.')[1]) )

   return dataOnLine
         
############################
#  test
############################

def TEST_DeltaIsPositive():
   delta = datetime.timedelta(days = 1, seconds = 0, microseconds = 0)
   assert(DeltaIsPositive(delta) == True)

   delta = datetime.timedelta(days = 0, seconds = 1, microseconds = 0)
   assert(DeltaIsPositive(delta) == True)

   delta = datetime.timedelta(days = 0, seconds = 0, microseconds = 1)
   assert(DeltaIsPositive(delta) == True)

   delta = datetime.timedelta(days = -1, seconds = 100, microseconds = 0)
   assert(DeltaIsPositive(delta) == False)

   delta = datetime.timedelta(days = 0, seconds = -1, microseconds = 10)
   assert(DeltaIsPositive(delta) == False)

   delta = datetime.timedelta(days = 0, seconds = 0, microseconds = -5)
   assert(DeltaIsPositive(delta) == False)

def test():
   TEST_DeltaIsPositive()

############################
#  main
############################


def main():
   currentData = datetime.datetime(year = 2021, 
                                   month = 1,
                                   day = 4,
                                   hour = 0,
                                   minute = 1,
                                   second = 55,
                                   microsecond = 0)
   fileManager = FileManager(FILE_NAME, 2)
   
   currentLine = fileManager.getNextLine()
   print(currentLine)

   while(fileManager.fine != True):
      dataOnLine = generateTimeFromLine(currentLine)
      delta = dataOnLine - currentData
   
      if(DeltaIsPositive(delta)):
         currentData = currentData + datetime.timedelta(seconds=1)
      else:         
         currentLine = fileManager.getNextLine()
         if(currentLine is not None):
            print(currentLine)



if __name__ == "__main__":
   main()
   #test()

