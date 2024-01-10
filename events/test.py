from broker import *
from messages import *
from algorithm import *


def dispatchFunction(message):
   algorithm.messageHandler(message)
   

def test1():
   firstMax = Entry(0, 1)
   firstMax.absoluteTimestamp = 0
   secondMax = Entry(1, 1.1)
   secondMax.absoluteTimestamp = 1
   firstMin = Entry(2, 0.1)
   firstMin.absoluteTimestamp = 2
   secondMin = Entry(3, 0.2)
   secondMin.absoluteTimestamp = 3

   message = Message()
   message.header.sender = SENDER_DATA
   message.header.type = NEW_DATA_ARRIVED
   message.payload = {
      "ultimo": 0.5,
      "time": {
         "tempo assoluto": 4
      }
   }

   algorithm.maxPoints.addItem(firstMax)
   algorithm.maxPoints.addItem(secondMax)
   algorithm.minPoints.addItem(firstMin)
   algorithm.minPoints.addItem(secondMin)

   broker_setDispatchFunction(dispatchFunction)
   broker.dispatch(message)

   algorithm.callback = algorithm.cb_inIdleRegion
   algorithm.manager()

   assert(algorithm.callback == algorithm.cb_inIdleRegion)
   




if __name__ == "__main__":
   test1()