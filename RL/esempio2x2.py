import numpy as np


grid = [
   [0, 0],
   [0, 0]
]


UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

B = [0, 1]


def nextState(action, currentState):
   
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

def reward(action, currentState):
   r = 0
   
   ns = nextState(action, currentState)
   if(ns == B):
      r = 5

   return r

NUMBER_COLUMN = 2
NUMBER_ROW = 2
GAMMA = 0.7

def findBestPolicy(V):
   
   policy = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )
   
   for i in range(NUMBER_COLUMN):
      for j in range(NUMBER_ROW):
         currentState = [i, j]
         
         bestReward = -1000
         bestAction = 0
         for action in range(4):
            ns = nextState(action, currentState)

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

  
def main():
   V = computeValueForUniformPolicy()
   np.set_printoptions(precision = 1)   
   print(V)
   


if __name__ == "__main__":
   main()
   

