
import numpy as np

#vedi video "policy iteration"

'''
matrice 4x4
lo stato finale è la posizione in alto a sx
quando arrivo ho come reward 1
ci sono dei muri, se li colpisco ho come reward -10
gli stati sono le possibili posizioni della matrice

azioni: 4 possibili direzioni
   se colpisco una parete rimango nello stesso stato
'''

rewards = [
   [0, 0, 0, 0],
   [0, 0, 0, 0],
   [0, 0, 0, 0],
   [0, 0, 0, 0],
]

TERMINAL_STATES = [ 
   [0, 0], 
  # [3, 3]
     ]

BLUE_STATES = [
   [0, 1], [0, 2], [0, 3],
   [2, 0], [2, 1], [2, 2]
]


UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

NUMBER_COLUMN = 4
NUMBER_ROW = 4

GAMMA = 1

def initRandomPolicy():
   policy = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )
   policy = np.ndarray.tolist(policy)
   
   for i in range(NUMBER_ROW):
      for j in range(NUMBER_COLUMN):
         policy[i][j] = [0.25, 0.25, 0.25, 0.25]
   
   return policy

def nextState(currentState, action):
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

   if(nextState[1] > NUMBER_COLUMN - 1):
      nextState[1] = NUMBER_COLUMN - 1
   if(nextState[1] < 0):
      nextState[1] = 0

   return nextState

def computeV(policy):
   V = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )
   keepWorking = True

   while(keepWorking):
      V_prime = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )
      
      for i in range(NUMBER_ROW):
         for j in range(NUMBER_COLUMN):
            currentState = [i, j]

            if(currentState in TERMINAL_STATES):
               pass
            else:
               sum = 0
               for action in range(4):
                  ns = nextState(currentState, action)
                  r = reward(currentState, action)
                  p = policy[i][j][action]
                  expectedValueInNextState = V[ns[0]][ns[1]]

                  sum += p * (r + GAMMA * expectedValueInNextState)
               
               V_prime[i][j] = sum

      if(abs(V - V_prime).sum() < 0.001):
         keepWorking = False

      V = np.copy(V_prime)
      print(V)
      
   return V

def computePolicy(V):
   newPolicy = initRandomPolicy()

   for i in range(NUMBER_ROW):
      for j in range(NUMBER_COLUMN):
         bestExpectedReward = -1000
         
         for action in range(4):
            ns = nextState([i, j], action)
            r = reward([i, j], action)
            expectedReward = r + GAMMA * V[ns[0]][ns[1]]

            if(expectedReward > bestExpectedReward):
               bestExpectedReward = expectedReward

         p = [0, 0, 0, 0]

         for action in range(4):
            ns = nextState([i, j], action)
            r = reward([i, j], action)
            expectedReward = r + GAMMA * V[ns[0]][ns[1]]

            if(expectedReward == bestExpectedReward):
               p[action] = 1

         p = normalizeArray(p)

         newPolicy[i][j] = p.copy()
   
   return newPolicy

def policyToAction(policy):
   matrix = np.zeros( (NUMBER_ROW, NUMBER_COLUMN) )

   for i in range(NUMBER_ROW):
      for j in range(NUMBER_COLUMN):
         actions = policy[i][j]
         a = actions.index(max(actions))
         matrix[i][j] = a

   return matrix

def normalizeArray(array):
   s = sum(array) 
   if(s > 1):
      for k in range(len(array)):
         array[k] = array[k] / s
   return array

def reward(currentState, action):
   ns = nextState(currentState, action)
   
   nextPosition = [ns[0], ns[1]]

   if(nextPosition in BLUE_STATES):
      return -10
   else:
      return -1

def main():
   np.set_printoptions(precision = 1)   
   
   policy = initRandomPolicy()
   V = np.zeros((NUMBER_ROW, NUMBER_COLUMN))

   keepgoing = True

   while(keepgoing):
      V = computeV(policy)
      newPolicy = computePolicy(V)
      print(V)
      #print(policy)
      print(policyToAction(policy))

      if(newPolicy == policy):
         keepgoing = False
      
      policy = newPolicy

         

if __name__ == "__main__":
   main()