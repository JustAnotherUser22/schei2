

'''
file con tutti i tipi di messaggi e pacchetti disponibili
'''

# valori del campo "sender" e "to"
SENDER_UNDEFINED = "undefined"
SENDER_DATA = "data"
SENDER_ALGORITHM = "algorithm"
SENDER_MANAGER = "manager"
SENDER_APPLICATION = "application"
PLOTTER = "plotter"

#valori del campo "type"
TYPE_UNDEFINED = "undefined"
SIGNAL_BUY = "buy"
SIGNAL_SELL = "sell"

NEW_DATA_ARRIVED = "new data arrived"
ORDER_HAS_BEEN_CLOSED = "order has been closed"
NEW_MOVING_AVERAGE_COMPUTED = "new moving average computed"
NEW_MACD_COMPUTED = "new macd computed"

MARKET_IS_OPEN = "market is open"
MARKET_IS_CLOSE = "market is close"

RESET = "need to reset"


class Message:
   def __init__(self):
      self.header = Header()
      self.payload = 0

class Header:
   def __init__(self):
      self.sender = SENDER_UNDEFINED
      self.to = SENDER_UNDEFINED
      self.type = TYPE_UNDEFINED

   #def __init__(self, sender, to):
   #   self.sender = 0
   #   self.to = 0

class Payload:
   def __init__(self):
      pass