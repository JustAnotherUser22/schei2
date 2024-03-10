


BUY = 'buy'
SELL = 'sell'



class Order:
   def __init__(self):
      self.openValue = 0
      self.closeValue = 0
      self.openedAtTime = 0
      self.closedAtTime = 0
      self.positionType = 0
      #self.takeProfit = 0
      #self.stopLoss = 0

   def reset(self):
      self.openValue = 0
      self.closeValue = 0
      self.openedAtTime = 0
      self.closedAtTime = 0
      self.positionType = 0
      #self.takeProfit = 0
      #self.stopLoss = 0
