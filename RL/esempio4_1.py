import numpy as np


#esempio sul libro
grid = [
         [ 0, 0, 0, 0],
         [ 0, 0, 0, 0],
         [ 0, 0, 0, 0],
         [ 0, 0, 0, 0],
       ]

TERMINAL_STATE_1 = [0, 0]
TERMINAL_STATE_2 = [3, 3]

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

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
   return -1

NUMBER_COLUMN = 4
NUMBER_ROW = 4
GAMMA = 1

def computeValueForUniformPolicy():
   V = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )
   keepWorking = True

   while(keepWorking):
      V_prime = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )

      for i in range(NUMBER_COLUMN):
         for j in range(NUMBER_ROW):
            currentState = [i, j]

            if(currentState == TERMINAL_STATE_1):
               pass
            elif(currentState == TERMINAL_STATE_2):
               pass
            else:
               sum = 0
               for action in range(4):
                  ns = nextState(action, currentState)
                  r = reward(action, currentState)
                  expectedValueInNextState = V[ns[0]][ns[1]]

                  value = (1 / 4) * (r + GAMMA * expectedValueInNextState)

                  sum += value
               
               V_prime[i][j] = sum
      
      if(abs(V - V_prime).sum() < 0.001):
         keepWorking = False

      V = np.copy(V_prime)  
      print(V)  

   return V

def findPolicyFromValue(V):
   policy = np.zeros( (4, 4) )

   for i in range(NUMBER_COLUMN):
      for j in range(NUMBER_ROW):

         currentState = [i, j]        
         if(currentState == TERMINAL_STATE_1):
            pass
         elif(currentState == TERMINAL_STATE_2):
            pass
         else:
            bestAction = 0
            bestReward = -1000
            for action in range(4):
               ns = nextState(action, [i, j])

               reward = V[ns[0]][ns[1]]

               if(reward > bestReward):
                  bestReward = reward
                  bestAction = action
               elif(reward == bestReward):
                  bestAction = str(bestAction) + str(action)
            
            policy[i][j] = bestAction

   return policy


  
def main():
   np.set_printoptions(precision = 1)   
   V = computeValueForUniformPolicy()   
   print(V)
   p = findPolicyFromValue(V)
   print(p)


if __name__ == "__main__":
   main()
   

