import time 
import datetime

start = datetime.datetime.now()
time.sleep(2)
stop = datetime.datetime.now()

print("start = " + str(start))
print("stop = " + str(stop))

delta = stop - start

print("delta = " + str(delta))