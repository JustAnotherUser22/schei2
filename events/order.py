

class Order:
   def __init__(self):
      self.openValue = 0
      self.closeValue = 0
      self.openedAtTime = 0
      self.closedAtTime = 0
      self.positionType = 0
      self.takeProfit = 0
      self.stopLoss = 0

   def reset(self):
      self.openValue = 0
      self.closeValue = 0
      self.openedAtTime = 0
      self.closedAtTime = 0
      self.positionType = 0
      self.takeProfit = 0
      self.stopLoss = 0

   def OpenPosition(self, positionType, openValue, timeStamp, takeProfit, stopLoss):
      self.positionType = positionType
      self.openValue = openValue
      self.openedAtTime = timeStamp
      self.takeProfit = takeProfit
      self.stopLoss = stopLoss