import sys
sys.path.insert(1, "schei2/EURUSD/dataFolder")

from broker import *
from messages import *
import dataFiles

'''
file che si occupa di leggere i dati grezzi in arrivo e di
formattarli correttamente per inviarli a chi li deve gestire

il payload del messaggio inviato è di questo tipo
header : {
   sender = SENDER_DATA
   type = NEW_DATA_ARRIVED
   }
payload : {
   "time": {
      "year": ,
      "month": ,
      "day": ,
      "hour": ,
      "minute": ,
      "second": ,
      "tick": ,
      "tempo assoluto": 
      },
   "apertura": ,
   "massimo": ,
   "minimo": ,
   "ultimo": ,
   "vol.": ,      
   }
'''

class DataReader:
   def __init__(self, broker):
      self.lines = 0
      self.counter = 0
      self.dataEnded = False
      self.callback = self.OpenFile
      self.broker = broker

   def manager(self):
      self.callback()

   def messageHandler(self, message):
      if(message.header.type == RESET):
         tmpBroker = self.broker
         self.__init__(tmpBroker)


   def OpenFile(self):
      #filePath = "D:\script\events\EUR_USD Dati Storici 2022.csv"
      #filePath = "C:/Users/Marco/Documents/python/supAndRes/EURUSD_M1_2022_02.csv"
      
      #filePath = "D:\script\schei2\supAndRes\EURUSD_M1_2022_onlyFebruary.csv"
      filePath = "D:\script\schei2\supAndRes\DAT_ASCII_EURUSD_T_2022_onlyFebruary.csv"
      #filePath = dataFiles.BASE_PATH + "DAT_ASCII_EURUSD_M1_2022_window_100.csv"
      
      #print("sto per caricare i dati")

      f = open(filePath, 'r')
      lines = f.readlines()
      lines.pop(0)   #rimuovi prima riga che è header
      #lines.reverse()

      #origianel
      #lines = lines[121290 : 369117]   #da 3 a 7
      lines = lines[0 : 119401]
      
      self.lines = lines
      self.callback = self.scanData
      self.counter = 0
      f.close()

      #print("finito")
      #print("caricati {0} dati".format(len(lines)))
      
   def scanData(self):
      length = len(self.lines) #500
      
      if(self.counter < length):
         line = self.lines[self.counter]
         #data = parseLine(line, self.counter)
         #data = parseLineFormAnotherFormat(line, self.counter)
         #data = parseLineFormTickFormat(line, self.counter)   #origianle
         data = unAltroParser(line, self.counter)
         self.publish(data)
         self.counter += int(1)
      else:
         self.dataEnded = True

   def publish(self, data):
      message = Message()
      message.header.sender = SENDER_DATA
      message.header.type = NEW_DATA_ARRIVED
      message.payload = data
      self.broker.dispatch(message)

def parseLine(line, counter):
   info = line.split("\",\"")
   for i in range(len(info)):
      info[i] = info[i].replace("\"", "")
      info[i] = info[i].replace("\'", "")
      info[i] = info[i].replace("\n", "")
      info[i] = info[i].replace(",", ".")

   timeInfo = info[0].split('.')
   
   timeDictionary = {
      "year": int(timeInfo[2]),
      "month": int(timeInfo[1]),
      "day": int(timeInfo[0]),
      "hour": int(-1),
      "minute": int(-1),
      "second": int(-1),
      "tick": int(-1),
      "tempo assoluto": int(counter)
   }

   dictionary = {
      #"data": info[0],
      "time": timeDictionary,
      "ultimo": float(info[1]),
      "apertura": float(info[2]),
      "massimo": float(info[3]),
      "minimo": float(info[4]),
      "vol.": info[5],
      "var. %": info[6],      
   }
   
   return dictionary

def parseLineFormAnotherFormat(line, counter):
   info = line.split(";")
   for i in range(len(info)):
      info[i] = info[i].replace("\"", "")
      info[i] = info[i].replace("\'", "")
      info[i] = info[i].replace("\n", "")
      info[i] = info[i].replace(",", ".")
   
   timeStamp = info[0].split(" ")

   timeDictionary = {
      "year": int(timeStamp[0][0:4]),
      "month": int(timeStamp[0][4:6]),
      "day": int(timeStamp[0][6:8]),
      "hour": int(timeStamp[1][0:2]),
      "minute": int(timeStamp[1][2:4]),
      "second": int(timeStamp[1][4:8]),
      "tick": int(-1),
      "tempo assoluto": int(counter)
   }

   dictionary = {
      "time": timeDictionary,
      "apertura": float(info[1]),
      "massimo": float(info[2]),
      "minimo": float(info[3]),
      "ultimo": float(info[4]),
      "vol.": info[5],      
   }
   
   return dictionary

def parseLineFormTickFormat(line, counter):
   info = line.split(",")
   for i in range(len(info)):
      info[i] = info[i].replace("\"", "")
      info[i] = info[i].replace("\'", "")
      info[i] = info[i].replace("\n", "")
      info[i] = info[i].replace(",", ".")
   
   timeStamp = info[0].split(" ")

   timeDictionary = {
      "year": int(timeStamp[0][0:4]),
      "month": int(timeStamp[0][4:6]),
      "day": int(timeStamp[0][6:8]),
      "hour": int(timeStamp[1][0:2]),
      "minute": int(timeStamp[1][2:4]),
      "second": int(timeStamp[1][4:6]),
      "tick": int(timeStamp[1][6:9]),
      "tempo assoluto": int(counter)
   }

   dictionary = {
      "time": timeDictionary,
      "ultimo": float(info[2]),      
   }
   
   return dictionary

def unAltroParser(line, counter):
   info = line.split(",")

   timeStamp = info[0].split(" ")

   
   timeDictionary = {
      "year": int(timeStamp[0][0:4]),
      "month": int(timeStamp[0][4:6]),
      "day": int(timeStamp[0][6:8]),
      "hour": int(timeStamp[1][0:2]),
      "minute": int(timeStamp[1][2:4]),
      "second": int(timeStamp[1][4:8]),
      "tick": int(-1),
      "tempo assoluto": int(counter)
   }
   
   '''
   timeDictionary = {
      "data": info[0],
      "tempo assoluto": int(counter)
   }
   '''
   
   dictionary = {
      "time": timeDictionary,
      "ultimo": float(info[2]),      
   }
   
   return dictionary


#dataReader = DataReader()


