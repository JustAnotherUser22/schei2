import pandas as pd
from ta.trend import MACD
import ta
import matplotlib.pyplot as plt

data = pd.read_csv("pandas/DAT_ASCII_EURUSD_M1_2022_gennaio.csv")

serie = data.iloc[:, 1]
signal = MACD(close = serie)

m = signal.macd_signal()

plt.plot(serie)
plt.plot(signal._emafast)
print(len(signal._emafast))
plt.show()