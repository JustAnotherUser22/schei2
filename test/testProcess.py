import multiprocessing
import datetime
import time
from testThread import INITIAL_COUNTER_VALUE
from testThread import functionThatComputeSomething
from testThread import functionToRunInProcess

def processTestWithRealFunction():
   '''
   i processi iniziano e terminano insieme e il tempo impiegato è pari a quello di 1 solo processo
   '''
   p1 = multiprocessing.Process(target = functionThatComputeSomething, args = ("p1", INITIAL_COUNTER_VALUE))
   p2 = multiprocessing.Process(target = functionThatComputeSomething, args = ("p2", INITIAL_COUNTER_VALUE))
   
   p1.start()
   p2.start()
   
   p1.join()
   p2.join()
   
   print("end")

def processTest():
   '''
   in questo test i processi partono in contemporanea e terminano insieme
   nella realtà questo può non essere vero dal momento che esiste un overhead per iniziare, gestire e terminare un processo
   '''
   p1 = multiprocessing.Process(target = functionToRunInProcess, args = ("p1", ))
   p2 = multiprocessing.Process(target = functionToRunInProcess, args = ("p2", ))
   #p3 = multiprocessing.Process(target = functionToRunInProcess, args = ("p3", ))
   #p4 = multiprocessing.Process(target = functionToRunInProcess, args = ("p4", ))

   p1.start()
   p2.start()
   #p3.start()
   #p4.start()

   p1.join()
   p2.join()
   #p3.join()
   #p4.join()

   print("end")

def main():
   functionThatComputeSomething("aaa", INITIAL_COUNTER_VALUE)
   #functionToRunInProcess("from main")

   processTestWithRealFunction()
   #processTest()

if __name__ == "__main__":
   main()