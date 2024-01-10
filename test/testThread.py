
import threading
import datetime
import time

#questo e l'altro esempio sono presi da qui
#https://www.geeksforgeeks.org/difference-between-multithreading-vs-multiprocessing-in-python/

INITIAL_COUNTER_VALUE = 200000000

def functionThatComputeSomething(processName, initialCounter):
   start = datetime.datetime.now()
   print("{0} start at {1}".format(processName, start))

   while(initialCounter > 0):
      initialCounter -= 1

   delta = datetime.datetime.now() - start
   print("{0} end in {1}".format(processName, delta))


def functionToRunInProcess(processName):
   start = datetime.datetime.now()
   print("{0} start at {1}".format(processName, start))

   time.sleep(5)

   delta = datetime.datetime.now() - start
   print("{0} end in {1}".format(processName, delta))



def testWithRealFunctions():
   '''
   i thread partono insieme e terminano insieme, ma il tempo impiegato totale è pari alla somma delle due funzioni
   '''
   t1 = threading.Thread( target = functionThatComputeSomething, args = ("thread-1", INITIAL_COUNTER_VALUE) )
   t2 = threading.Thread( target = functionThatComputeSomething, args = ("thread-2", INITIAL_COUNTER_VALUE) )

   t1.start()
   t2.start()

   t1.join()
   t2.join()

   print("end")

def testWithSleepFunctions():
   '''
   anche questi partono in contemporanea come i processi e il tempo totale è quello di 1 solo processo
   '''
   t1 = threading.Thread( target = functionToRunInProcess, args = ("thread-1", ) )
   t2 = threading.Thread( target = functionToRunInProcess, args = ("thread-2", ) )

   t1.start()
   t2.start()

   t1.join()
   t2.join()

   print("end")



def main():
   #functionThatComputeSomething("from main", INITIAL_COUNTER_VALUE)
   #functionToRunInProcess("from main")

   #testWithRealFunctions();
   testWithSleepFunctions()

if __name__ == "__main__":
   main()