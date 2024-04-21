import numpy as np


#esempio sul libro
grid = [
         [ 0, 0, 0, 0, 0],
         [ 0, 0, 0, 0, 0],
         [ 0, 0, 0, 0, 0],
         [ 0, 0, 0, 0, 0],
         [ 0, 0, 0, 0, 0],
       ]


UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

A = [0, 1]
B = [0, 3]
A_prime = [4, 1]
B_prime = [2, 3]

def nextState(action, currentState):
   
   if(currentState == A):
      nextState = A_prime
   elif(currentState == B):
      nextState = B_prime
   else:
      row = currentState[0]
      column = currentState[1]
      nextState = [0, 0]

      if(action == UP):
         nextState[0] = row - 1
         nextState[1] = column
      elif(action == DOWN):
         nextState[0] = row + 1
         nextState[1] = column
      elif(action == LEFT):
         nextState[0] = row
         nextState[1] = column - 1
      elif(action == RIGHT):
         nextState[0] = row
         nextState[1] = column + 1

      #todo: ok per matrici quadrate, ma controlla comunque questo
      if(nextState[0] > NUMBER_ROW - 1):
         nextState[0] = NUMBER_ROW - 1
      if(nextState[0] < 0):
         nextState[0] = 0

      if(nextState[1] > NUMBER_ROW - 1):
         nextState[1] = NUMBER_ROW - 1
      if(nextState[1] < 0):
         nextState[1] = 0

   return nextState

def rewardInState(currentState):
   row = currentState[0]
   column = currentState[1]
   return grid[row][column]

def reward(action, currentState):
   r = 0
   
   if(currentState == A):
      r = 10
   elif(currentState == B):
      r = 5
   else:
      ns = nextState(action, currentState)
      if(ns == currentState):
         r = -1

   return r

NUMBER_COLUMN = 5
NUMBER_ROW = 5
GAMMA = 0.9

def findBestPolicy(V):
   
   policy = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )
   
   for i in range(NUMBER_COLUMN):
      for j in range(NUMBER_ROW):
         currentState = [i, j]
         
         bestReward = -1000
         bestAction = 0
         for action in range(4):
            ns = nextState(action, currentState)

            #la "reward" sarebbe il valore atteso che mi aspetto di avere in un dato stato, e voglio massimizzare questo valore
            reward = V[ns[0]][ns[1]]
            if(reward >= bestReward):
               bestReward = reward
               bestAction = action
         
         policy[i][j] = bestAction
   
   return policy

def computeValueForUniformPolicy():
   V = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )
   keepWorking = True

   while(keepWorking):
      V_prime = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )

      for i in range(NUMBER_COLUMN):
         for j in range(NUMBER_ROW):
            currentState = [i, j]

            sum = 0
            for action in range(4):
               ns = nextState(action, currentState)
               r = reward(action, currentState)
               expectedValueInNextState = V[ns[0]][ns[1]]

               value = (1 / 4) * (r + GAMMA * expectedValueInNextState)

               sum += value
            
            V_prime[i][j] += sum
      
      if(abs(V - V_prime).sum() < 0.001):
         keepWorking = False

      V = np.copy(V_prime)  
      #print(V)  

   return V

def computeValueForBestPolicy():
   V = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )
   keepWorking = True

   while(keepWorking):
      V_prime = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )

      for i in range(NUMBER_COLUMN):
         for j in range(NUMBER_ROW):
            currentState = [i, j]

            maxAction = -1000
            for action in range(4):
               ns = nextState(action, currentState)
               r = reward(action, currentState)
               expectedValueInNextState = V[ns[0]][ns[1]]

               value = r + GAMMA * expectedValueInNextState

               if(value > maxAction):
                  maxAction = value
            
            V_prime[i][j] += maxAction
      
      if(abs(V - V_prime).sum() < 0.001):
         keepWorking = False

      V = np.copy(V_prime)  
      #print(V)  

   return V

  
def main():
   V = computeValueForBestPolicy()
   np.set_printoptions(precision = 1)   
   print(V)
   #policy = findBestPolicy(V)
   #print(policy)




if __name__ == "__main__":
   main()
   

