from time import sleep
from random import random
from threading import Thread
import threading
from multiprocessing import Process
import multiprocessing

#https://superfastpython.com/thread-mutex-lock/
#https://superfastpython.com/multiprocessing-mutex-lock-in-python/


# work function
def taskForThread(lock, identifier, value):
   # acquire the lock
   with lock:
      print(f'>thread {identifier} got the lock, sleeping for {value}')
      sleep(value)
 
 # work function
def taskForProcess(lock, identifier, value):
    # acquire the lock
    with lock:
        print(f'>process {identifier} got the lock, sleeping for {value}')
        sleep(value)


def mutexInThread():
   # create a shared lock
   lock = threading.Lock()
   # start a few threads that attempt to execute the same critical section
   for i in range(10):
      # start a thread
      Thread(target = taskForThread, args = (lock, i, random())).start()
      
   # wait for all threads to finish...


def mutexInProcess():
   # create the shared lock
   lock = multiprocessing.Lock()
   # create a number of processes with different sleep times
   processes = [Process(target = taskForProcess, args = (lock, i, random())) for i in range(10)]
   # start the processes
   for process in processes:
      process.start()
   # wait for all processes to finish
   for process in processes:
      process.join()

def main():
   #mutexInThread()
   mutexInProcess()

if __name__ == "__main__":
   main()