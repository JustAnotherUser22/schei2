


DOUBLE_EMA = "double ema"

FIXED_LIMTIS = "FIXED_LIMTIS"
SIGNALS_FROM_ALGO = 'SIGNALS_FROM_ALGO'


class Configuration:

   def __init__(self):
      self.configurationUsed = "none"
      self.createLog = False
      self.fastWindow = 10000
      self.slowWindow = 20000
      self.stopBy = "FIXED_LIMTIS"

      self.takeProfit = 0.001
      self.stopLoss = 0.002


config = Configuration()

