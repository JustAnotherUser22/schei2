
import random
import matplotlib.pyplot as plt

MINIMUM_BET = 1
DELTA = 0.1

def main():
   account = 100
   log = []
   log.append(account)
   
   #random.seed(42)

   currentbet = 10
   positiveOutcome = True

   for i in range(10000):
      n = random.randrange(0, 36+1, 1)

      if(n >= 1 and n <= 18):
         account += currentbet
         positiveOutcome = True
      else:
         account -= currentbet
         positiveOutcome = False

      if(positiveOutcome == True):
         currentbet -= DELTA
         if(currentbet < MINIMUM_BET):
            currentbet = MINIMUM_BET
      else:
         currentbet += DELTA
      

      log.append(account)

   plt.plot(log)
   plt.show()
         

      
def factorial(n):
   if(n == 0):
      return 1
   return n*factorial(n-1)

def binomialCoefficient(k, n):
   return int((factorial(n)/factorial(k)/factorial(n-k)))

def bernulliDistribution(k, n, p):
   pn = 1-p
   k = int(k)
   n = int(n)
   return binomialCoefficient(k, n) * (p**k) * (pn**(n-k))

if __name__ == "__main__":
   main()
   
   p = 18/37
   n = 1.9*bernulliDistribution(2, 2, p) + 0.1 *bernulliDistribution(1, 2, p) - 2.1*bernulliDistribution(0,2,p)
   print(n)
   
   