
import random
import matplotlib.pyplot as plt


def main():
   account = 100
   log = []
   log.append(account)
   
   #random.seed(42)

   currentbet = 0.1
   positiveOutcome = True

   for i in range(100000):
      n = random.randrange(0, 36+1, 1)

      if(positiveOutcome == True):
         currentbet = 0.1
      else:
         currentbet = currentbet * 5
      
      if(n >= 1 and n <= 30):
         account += currentbet
         positiveOutcome = True
      else:
         account -= (5 * currentbet)
         positiveOutcome = False

      log.append(account)

   plt.plot(log)
   plt.show()
         

      


if __name__ == "__main__":
   main()