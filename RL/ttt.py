import numpy as np

EMPTY = 0
P1 = 1
P2 = 2

'''
P1 parte per primo
le configurazioni valide sono quindi quelle in cui:
   - è tutto vuoto
   - ci sono più P2 che P1
   - al massimo c'è un simbolo P2 in più di quelli P1

state: una delle possibili configurazioni della matrice 3x3
   può essere una matrice 3x3
   può essere un vettore 1x9
   può essere un indice univocamente (si spera) associato a un vettore 1x9
azione: inserire un simbolo in una locazione vuota della matrice 3x3
   un' azione è un numero tra 0 e 8 compresi, indicante la locazione in cui andrà inserito il simbolo
reward: 1 se vinco io, -1 se vince l'altro
'''

def stateIsRotation(state):
   #controlla se lo stato attuale è una "rotazione" di uno stato già esistente
   pass

def isGivenPlayerWinningInGivenState(player, state):
   matrix = np.reshape(state, (3,3))
   toReturn = False

   for i in range(3):
      if(matrix[i][0] == player and matrix[i][1] == player and matrix[i][2] == player):
         toReturn = True

   for i in range(3):
      if(matrix[0][i] == player and matrix[1][i] == player and matrix[2][i] == player):
         toReturn = True
   
   if(matrix[0][0] == player and matrix[1][1] == player and matrix[1][1] == player):
      toReturn = True

   return toReturn

def rewardInState(state):
   if(isGivenPlayerWinningInGivenState(P1, state)):
      return 1
   elif(isGivenPlayerWinningInGivenState(P1, state)):
      return -1
   else:
      return 0

def isValidState(state):
   s = np.reshape(state, (3,3))
   
   numberOfP1 = 0
   numberOfP2 = 0

   for i in range(9):
      if(state[i] == P1):
         numberOfP1 += 1
      elif(state[i] == P2):
         numberOfP2 += 1
   
   if(numberOfP1 > numberOfP2):
      return False

   if(abs(numberOfP2 - numberOfP1) > 1):
      return False
   
   return True

def allActionsforGivenState(state):
   allActions = []
   for i in range(9):
      if(state[i] == 0):
         allActions.append(i)
   
   return allActions

def nextState(allStates, state, action):
   currentState = state
   nextState = currentState
   nextState[action] = 1
   index = allStates.index(nextState)
   return index

def reward(action, currentState):

   ns = nextState(allStates, currentState, action)

   return rewardInState(ns)


def generateAllStates():

   allStates = []

   for values in np.ndindex(3, 3, 3, 3, 3, 3, 3, 3, 3):
      #state = tuple(values)
      state = values
      if(isValidState(state)):
         allStates.append(state)

   return allStates

def probabilityOfCertainActionInGivenState(state):
   howManyPossibleStates = generateAllStates()
   return 1 / howManyPossibleStates

def possibleNextStateOfP2(state):
   allNextStates = []
   emptyCounter = 0

   #for i in state:
   #   if (i == EMPTY):
   #      emptyCounter += 1
   
   for i in range(len(state)):
      if (state[i] == EMPTY):
         local = np.copy(state)
         local[i] = P2
         allNextStates.append(local)
   
   return allNextStates



if __name__ == "__main__":
   allStates = generateAllStates()

   V = np.zeros(len(allStates))
   
   
   while(True):
      V_prime = np.zeros(len(allStates))

      for i in allStates:
         currentState = i
         currentStateIndex = allStates.index(currentState)
         sum = 0
         actions = allActionsforGivenState(currentState)
         numberOfActions = len(actions)

         for action in actions:
            
            state = list(currentState)
            #eseguo la mia azione
            state[action] = P1
            #possibili azioni dell'altro player
            states = possibleNextStateOfP2(state)
            
            ns = nextState(allStates, currentState, action)
            r = reward(action, currentState)
            expectedValueInNextState = V[ns[0]][ns[1]]

            sum += 1 / numberOfActions + ( r + 0.9 * expectedValueInNextState)

         V_prime[i] = V[i] + sum
   

