
from messages import *
from ta.trend import MACD
import numpy as np
import pandas as pd


class myMACD:
   def __init__(self, broker):
      self.data = []

      #parameters
      #self.fast = 12
      #self.signal = 9
      #self.slow = 26
      self.fast = 50
      self.signal = 22
      self.slow = 110

      #external data
      self.needToBuy = False
      self.needToSell = False
      self.lastValue = []
      self.broker = broker
      self.cb_signalLineCrossover = self.cb_signalCrossover_idle
      self.cb_zeroCrossover = self.cb_zeroCrossover_idle

      #robe locali
      self.lastHistogram = 0
      self.lastMacd = 0
      self.signalCounter = 0
      self.zeroCounter = 0
      self.ZERO_COUNTER_THRESHOLD = 20
      self.SIGNAL_COUNTER_THRESHOLD = 20
      

   def manager(self):
      #eseguo operazioni solo quando arriva un nuovo dato
      pass
      
   def messageHandler(self, message):
      if(message.header.type == NEW_DATA_ARRIVED):
         value = message.payload["ultimo"]
         time = message.payload["time"]
         self.data.append(value)

         dataLength = len(self.data)
         minimumLength = self.slow + self.signal - 1

         if(dataLength > minimumLength):
            self.processReceivedData(value, time)


   def processReceivedData(self, value, time):
      self.data.pop(0)
      macd, histogram, signal = self.computeMacd()
      macd = np.array(macd)
      histogram = np.array(histogram)
      signal = np.array(signal)
      #print(macd)
      #print(histogram)
      #print(signal)

      self.publicNewMACDEntry(macd[-1], signal[-1], histogram[-1])

      self.needToBuy = False
      self.needToSell = False      

      self.cb_signalLineCrossover(histogram[-1], value, time)
      self.cb_zeroCrossover(macd[-1], value, time)

      if(self.needToBuy == True and self.needToSell == True):
         oraSonoCazzi = True


   def cb_zeroCrossover_idle(self, macd, value, time):
      currentMacd = macd

      if(self.lastMacd < 0 and currentMacd > 0):
         self.zeroCounter = 0
         self.cb_zeroCrossover = self.cb_zeroCrossover_upCounting

      if(self.lastMacd > 0 and currentMacd < 0):
         self.zeroCounter = 0
         self.cb_zeroCrossover = self.cb_zeroCrossover_downCounting




   def cb_signalCrossover_idle(self, histogram, value, time):
      currentHistogram = histogram

      if(self.lastHistogram < 0 and currentHistogram > 0):
         self.signalCounter = 0
         self.cb_signalLineCrossover = self.cb_signalCrossover_upCounting

      if(self.lastHistogram > 0 and currentHistogram < 0):
         self.signalCounter = 0
         self.cb_signalLineCrossover = self.cb_signalCrossover_downCounting

      self.lastHistogram = currentHistogram

   def cb_signalCrossover_upCounting(self, histogram, value, time):
      if(histogram > 0):
         self.signalCounter += 1
         if(self.signalCounter == self.SIGNAL_COUNTER_THRESHOLD):
            self.cb_signalOverAverage(value, time)
      else:
         self.cb_signalLineCrossover = self.cb_signalCrossover_idle

   def cb_signalCrossover_downCounting(self, histogram, value, time):
      if(histogram < 0):
         self.signalCounter += 1
         if(self.signalCounter == self.SIGNAL_COUNTER_THRESHOLD):
            self.cb_signalUnderAverage(value, time)
      else:
         self.cb_signalLineCrossover = self.cb_signalCrossover_idle





   def cb_zeroCrossover_upCounting(self, histogram, value, time):
      if(histogram > 0):
         self.zeroCounter += 1
         if(self.zeroCounter == self.ZERO_COUNTER_THRESHOLD):
            self.cb_signalOverAverage(value, time)
      else:
         self.cb_signalLineCrossover = self.cb_signalCrossover_idle

   def cb_zeroCrossover_downCounting(self, histogram, value, time):
      if(histogram < 0):
         self.zeroCounter += 1
         if(self.zeroCounter == self.ZERO_COUNTER_THRESHOLD):
            self.cb_signalUnderAverage(value, time)
      else:
         self.cb_signalLineCrossover = self.cb_signalCrossover_idle
      



   def cb_signalOverAverage(self, value, time):
      self.needToBuy = True
      self.lastValue = {
                           "value": value,
                           "time": time
                        }
                
   def cb_signalUnderAverage(self, value, time):
      self.needToSell = True
      self.lastValue = {
                           "value": value,
                           "time": time
                        }
      
   def computeMacd(self):
      df = pd.DataFrame(self.data, columns = ['a'])
      df = df['a']
      porcodio = MACD(close = df, window_fast = self.fast, window_slow = self.slow, window_sign = self.signal)
      macd = porcodio.macd()
      histogram = porcodio.macd_diff()
      sign = porcodio.macd_signal()
      return macd, histogram, sign
   
   def publicNewMACDEntry(self, macd, signal, histogram):
      message = Message()
      message.header.type = NEW_MACD_COMPUTED
      message.header.to = PLOTTER
   
      dictionary = {
         "macd": macd,
         "signal": signal,
         "histogram": histogram
      }
      
      message.payload = dictionary
      self.broker.dispatch(message)
      




