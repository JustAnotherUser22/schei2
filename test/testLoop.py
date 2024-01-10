
#https://stackoverflow.com/questions/15902835/changing-iteration-variable-inside-for-loop-in-python

def changeValueInRange():
    
   firstTime = True

   for i in range(0,10):
      if(firstTime == True):
         firstTime = False
         i = 5
      print(i)

def changeValueInWhile():
       
   firstTime = True
   i = 0
   while(i < 10):
      if(firstTime == True):
         firstTime = False
         i = 5
      print(i)
      i += 1

def main():
   #changeValueInRange()
   changeValueInWhile()

if __name__ == "__main__":
    main()