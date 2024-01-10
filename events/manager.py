
from broker import *
from messages import *
from order import *
import copy

'''
manager che apre gli ordini quando riceve un comando e lo chiude quando raggiunge la
soglia di take profit o stop loss. segnali di apertura posizioni quando già una posizione è
aperta vengono ignorati
'''



class Manager:
   def __init__(self):
      self.callback = self.cb_noOrder
      self.lastValueReceived = None
      self.timestampLastData = None
      self.order = Order()
      self.canPerformOperation = True
      self.PROFIT_OR_STOP_DELTA = 0.0002

   def manager(self):
      #self.callback()
      pass

   def messageHandler(self, message):
      if(message.header.type == SIGNAL_BUY or
         message.header.type == SIGNAL_SELL):
         if(self.canPerformOperation == True):
            if(self.callback == self.cb_noOrder):
               openValue = message.payload["value"]
               timeData = message.payload["time"]
               #profitOrStopDelta = 0.0002
               if(message.header.type == SIGNAL_BUY):
                  takeProfit = round(openValue + self.PROFIT_OR_STOP_DELTA, 7)
                  stopLoss = round(openValue - self.PROFIT_OR_STOP_DELTA , 7)
                  self.order.OpenPosition("buy", openValue, timeData, takeProfit, stopLoss)
                  
               elif(message.header.type == SIGNAL_SELL):
                  takeProfit = round(openValue - self.PROFIT_OR_STOP_DELTA, 7)
                  stopLoss = round(openValue + self.PROFIT_OR_STOP_DELTA, 7)
                  self.order.OpenPosition("sell", openValue, timeData, takeProfit, stopLoss)
                  
               self.callback = self.cb_hasOrder

      elif(message.header.type == NEW_DATA_ARRIVED):
         self.lastValueReceived = float(message.payload["ultimo"])
         self.timestampLastData = message.payload["time"]
         self.callback()   #se non ho niente di aperto chiama la cb_idle (e non fa niente) altrimenti chiama la cb_hasOrder

      elif(message.header.type == MARKET_IS_OPEN):
         self.canPerformOperation = True

      elif(message.header.type == MARKET_IS_CLOSE):
         self.canPerformOperation = False

      elif(message.header.type == RESET):
         self.__init__()

   def cb_noOrder(self):
      return 0
   
   def cb_waitServerResponse(self):
      #se entro qui ho inviato la richiesta di apertura ordine al server e sto attendendo
      #una risposta, se la risposta è affermativa l'ordine è stato effettivamente aperto
      #altrimenti il processo non si è concluso correttamente e sono ancora senza ordini aperti
      if(True):
         self.callback = self.cb_hasOrder
      else:
         self.callback = self.cb_noOrder

   def cb_hasOrder(self):
      if(self.order.positionType == "buy"):
         if(self.isNeededToCloseBuyPosition()):            
            self.closeCurrentlyOpenOrder()
         
      elif(self.order.positionType == "sell"):
         if(self.isNeededToCloseSellPosition()):            
            self.closeCurrentlyOpenOrder()
   
   #####################
   # private functions
   #####################      

   def isNeededToCloseBuyPosition(self):
      return (self.lastValueReceived > self.order.takeProfit or  #è andata bene
               self.lastValueReceived < self.order.stopLoss)     #è andata male)

   def isNeededToCloseSellPosition(self):
      return (self.lastValueReceived < self.order.takeProfit or  #è andata bene
            self.lastValueReceived > self.order.stopLoss)     #è andata male

   def closeCurrentlyOpenOrder(self):
      if(self.canPerformOperation == True):
         self.callback = self.cb_noOrder
         self.order.closeValue = self.lastValueReceived
         self.order.closedAtTime = self.timestampLastData
         self.publishClosedOrder()

   def publishClosedOrder(self):
      message = Message()
      message.header.sender = SENDER_MANAGER
      message.header.type = ORDER_HAS_BEEN_CLOSED
      message.payload = copy.copy(self.order)
      broker.dispatch(message)      
      self.order.reset()


manager = Manager()


