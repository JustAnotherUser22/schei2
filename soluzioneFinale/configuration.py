


DOUBLE_EMA = "double ema"

FIXED_LIMTIS = "FIXED_LIMTIS"
SIGNALS_FROM_ALGO = 'SIGNALS_FROM_ALGO'
TRAILING_TAKE_PROFIT = "TRAILING_TAKE_PROFIT"


class Configuration:

   def __init__(self):
      self.configurationUsed = "none"
      self.createLog = False
      #self.fastWindow = 10000
      #self.slowWindow = 20000
      self.slowWindow = 42840
      self.fastWindow = 27860
      #self.stopBy = "FIXED_LIMTIS"
      self.stopBy = TRAILING_TAKE_PROFIT

      #self.takeProfit = 0.001
      #self.stopLoss = 0.002
      self.takeProfit = 0.0093
      self.stopLoss = 0.001#0.0013


config = Configuration()

