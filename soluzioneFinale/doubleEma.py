import math
import order
import configuration
from ta.trend import EMAIndicator
import pandas as pd



class Doubleema():
   def __init__(self, close, config):
      self.close = close
      self.config = config
      self.signals = createSignals(close, config)

      self.currentFast = 0
      self.currentSlow = 0

      self.signalGenerated = 0
      self.currentIndex = 0

      self.openAt = 0


   def allDataAreAvailable(self):
      i = self.currentIndex
      v1 = self.close[i]
      v2 = self.signals['slow'][i]
      if(math.isnan(v1) == False and 
         math.isnan(v2) == False and
         math.isnan(self.signals['fast'][i]) == False):
         return True


   def generateEntrySignal(self):
      i = self.currentIndex
      valueToReturn = False
      '''
      if(self.currentFast == 0 and
         self.currentSlow == 0):
         pass         
      else:
         if(self.currentFast < self.currentSlow and
            self.signals['fast'][i] > self.signals['slow'][i]):
            valueToReturn =  True
            self.signalGenerated = order.BUY
            self.openAt = self.close[i]
         if(self.currentFast > self.currentSlow and
            self.signals['fast'][i] < self.signals['slow'][i]):
            valueToReturn = True
            self.signalGenerated = order.SELL
            self.openAt = self.close[i]
      '''
      if(self.signals['fast'][i] > self.signals['slow'][i] and
         self.signals['fast'][i] - self.signals['slow'][i] > 0.0003):
         valueToReturn =  True
         self.signalGenerated = order.BUY
         self.openAt = self.close[i]
      if(self.signals['fast'][i] < self.signals['slow'][i] and
         self.signals['fast'][i] - self.signals['slow'][i] < -0.0003):
         valueToReturn = True
         self.signalGenerated = order.SELL
         self.openAt = self.close[i]
      

      self.updateValues(self.signals['fast'][i], self.signals['slow'][i])
      return valueToReturn
   


   def generateExitSignal(self):
      i = self.currentIndex
      valueToReturn = False
      
      if(self.config.stopBy == configuration.FIXED_LIMTIS):
         valueToReturn = self.checkIfCurrentValueIsOverStopLossOrTakeProfit()
      elif(self.config.stopBy == configuration.SIGNALS_FROM_ALGO):
         valueToReturn = self.checkIfAlgoProvidExitSignals()
      elif(self.config.stopBy == configuration.TRAILING_TAKE_PROFIT):
         valueToReturn = self.robaConTrailTakeProfit()

      self.updateValues(self.signals['fast'][i], self.signals['slow'][i])
      return valueToReturn
   

   def robaConTrailTakeProfit(self):
      i = self.currentIndex
      valueToReturn = False

      if(self.signalGenerated == order.BUY):
         if(self.close[i] > self.openAt + 0.0003):
            self.openAt = self.close[i]
         if(self.close[i] < self.openAt - self.config.stopLoss):
            valueToReturn =  True

      if(self.signalGenerated == order.SELL):
         if(self.close[i] < self.openAt - 0.0003):
            self.openAt = self.close[i]
         if(self.close[i] > self.openAt + self.config.stopLoss):
            valueToReturn =  True
      
      return valueToReturn


   def checkIfCurrentValueIsOverStopLossOrTakeProfit(self):
      i = self.currentIndex
      valueToReturn = False

      if(self.signalGenerated == order.BUY):
         if(self.close[i] > self.openAt + self.config.takeProfit or
            self.close[i] < self.openAt - self.config.stopLoss):
            valueToReturn =  True
      if(self.signalGenerated == order.SELL):
         if(self.close[i] < self.openAt - self.config.takeProfit or
            self.close[i] > self.openAt + self.config.stopLoss):
            valueToReturn =  True
      
         '''
         if(self.close[i] > self.openAt + 0.001 or
            self.close[i] > self.openAt - 0.001):
            valueToReturn =  True
         '''
         
      return valueToReturn

   def checkIfAlgoProvidExitSignals(self):
      i = self.currentIndex
      valueToReturn = False

      if(self.currentFast == 0 and
         self.currentSlow == 0):
         pass         
      else:
         if(self.currentFast < self.currentSlow and
            self.signals['fast'][i] > self.signals['slow'][i]):
            valueToReturn =  True
         if(self.currentFast > self.currentSlow and
            self.signals['fast'][i] < self.signals['slow'][i]):
            valueToReturn = True

      return valueToReturn
         


   def updateValues(self, fast, slow):
      self.currentFast = fast
      self.currentSlow = slow







def createSignals(close , config):
   slow = EMAIndicator(close = close, window = 20000)
   fast = EMAIndicator(close = close, window = 10000)
   slow = slow.ema_indicator()
   fast = fast.ema_indicator()
   data = {
      'fast': fast,
      'slow': slow
      }
   return pd.DataFrame(data)


