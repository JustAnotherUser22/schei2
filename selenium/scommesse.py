import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from dizionarioPagine import *
import time
import copy
import os
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd

class Singola:
   def __init__(self):
      self.uno = 0
      self.due = 0
      self.X = 0

class Doppia:
   def __init__(self):
      self.unoDue = 0
      self.dueX = 0
      self.unoX = 0
   
class Gol:
   def __init__(self):
      self.si = 0
      self.no = 0
          
class Bet:

   def __init__(self):
      self.squadra1 = ''
      self.squadra2 = ''
      self.singola = Singola()
      self.doppia = Doppia()
      self.gol = Gol()

   def printBet(self):
      print("{0} {1} {2} {3} {4}".format(self.squadra1, self.squadra2, self.singola.uno, self.singola.X, self.singola.due))

'''
data = {'origin': ['b', 'b', 's'],
            'team1': ['mi', 'mi', 'mi'],
            'team2': ['ju', 'ju', 'ju'],
            '1': [3, 3, 3],
            'X': [3, 3, 3],
            '2': [3, 3, 3],
            '1X': [3, 3, 3],
            'X2': [3, 3, 3],
            '12': [3, 3, 3],
            'gol si': [3, 3, 3],
            'gol no': [3, 3, 3]}

dataFrame = pd.DataFrame(data)
'''

dataFrame = pd.DataFrame({'origin': 0,
                           'team1': 0,
                           'team2': 0,
                           '1': 0,
                           'X': 0,
                           '2': 0,
                           '1X': 0,
                           'X2': 0,
                           '12': 0,
                           'gol si': 0,
                           'gol no': 0}, index = [0])


def appendDataToDataFrame(bet):
   
   row_index = dataFrame.index[(dataFrame['origin'] == bet.origin) &
                              (dataFrame['team1'] == bet.squadra1) &
                              (dataFrame['team2'] == bet.squadra2)].tolist()
   
   if(len(row_index) == 0):
      dataFrame.loc[len(dataFrame.index)] = [bet.origin, 
                                             bet.squadra1, 
                                             bet.squadra2, 
                                             bet.singola.uno, 
                                             bet.singola.X, 
                                             bet.singola.due,
                                             bet.doppia.unoX,
                                             bet.doppia.dueX,
                                             bet.doppia.unoDue,
                                             bet.golsi,
                                             bet.golno]  
   else:
      if((dataFrame.loc[row_index[0], '1'] != bet.singola.uno) |
         (dataFrame.loc[row_index[0], '2'] != bet.singola.due) |
         (dataFrame.loc[row_index[0], 'X'] != bet.singola.X) |
         (dataFrame.loc[row_index[0], '1X'] != bet.doppia.unoX) |
         (dataFrame.loc[row_index[0], 'X2'] != bet.doppia.dueX) |
         (dataFrame.loc[row_index[0], '12'] != bet.doppia.unoDue) ):
         dataFrame.loc[row_index[0], '1'] = bet.singola.uno
         dataFrame.loc[row_index[0], '2'] = bet.singola.due
         dataFrame.loc[row_index[0], 'X'] = bet.singola.X
         dataFrame.loc[row_index[0], '1X'] = bet.doppia.unoX
         dataFrame.loc[row_index[0], 'X2'] = bet.doppia.dueX
         dataFrame.loc[row_index[0], '12'] = bet.doppia.unoDue
   


def getBwin(driver):
   
   tutto = driver.find_elements(By.XPATH, "/html/body/vn-app/vn-dynamic-layout-slot[5]/vn-main/main/div/ms-main/div[1]/ng-scrollbar[2]/div/div/div/div/ms-main-column/div/ms-fixture-list/div/div[1]/div/div[1]/ms-grid/div")
   tabelle = tutto[0].find_elements(By.TAG_NAME, "ms-event-group")

   for tabella in tabelle:
      entry = tabella.find_elements(By.TAG_NAME, "ms-event")

      for e in entry:
         data = e.text.split('\n')

         if(len(data) > 10):
            bet = Bet()
            bet.squadra1 = data[0]
            bet.squadra2 = data[1]

            firstIndexOfValues = 2
            while('Oggi' in data[firstIndexOfValues] or
                  'Domani' in data[firstIndexOfValues] or
                  'Comincia' in data[firstIndexOfValues] or
                  '/' in data[firstIndexOfValues] or
                  'LIVE' in data[firstIndexOfValues] or
                  'Intervallo' in data[firstIndexOfValues] or
                  '1T' in data[firstIndexOfValues] or
                  '2T' in data[firstIndexOfValues] or
                  data[firstIndexOfValues] == '0' or
                  data[firstIndexOfValues] == '1' or
                  data[firstIndexOfValues] == '2' or
                  data[firstIndexOfValues] == '3'):
               firstIndexOfValues += 1

            i = firstIndexOfValues
            bet.singola.uno = data[i]
            bet.singola.X = data[i+1]
            bet.singola.due = data[i+2]
            bet.doppia.unoX = data[i+3]
            bet.doppia.dueX = data[i+4]
            bet.doppia.unoDue = data[i+5]
            bet.golsi = 0
            bet.golno = 0
            #bet.printBet()
            bet.origin = 'bwin'
            
            appendDataToDataFrame(copy.deepcopy(bet))

         else:
            pass
            #print("-- ERRORE --")


def getSisal(driver):
   allBet = []
        
   tutto = driver.find_elements(By.XPATH, "/html/body/main/div[2]/div/div/div[3]/div/div[1]/div[3]/div/div/div[2]/div/div/div/div[1]/div/div[3]/div[4]/div[2]")
   tabelle = tutto[0].find_elements(By.XPATH, "//div[@class='grid_mg-row-wrapper__usTh4 grid_noPromoAlert__U2MaM']")

   #while (True):
   for e in tabelle:
      data = e.text.split('\n')

      if(len(data) > 10):
         bet = Bet()
         bet.squadra1 = data[2]
         bet.squadra2 = data[3]
         bet.singola.uno = data[4]
         bet.singola.X = data[5]
         bet.singola.due = data[6]
         bet.doppia.unoX = data[7]
         bet.doppia.dueX = data[8]
         bet.doppia.unoDue = data[9]
         bet.golsi = 0
         bet.golno = 0
         
         #bet.printBet()
         bet.origin = 'sisal'
         allBet.append(copy.deepcopy(bet))
         appendDataToDataFrame(copy.deepcopy(bet))

      else:
         print("-- ERRORE --")


def checkOpportunity():
   dfcopy = copy.deepcopy(dataFrame)

   while(len(dfcopy) > 0):
      squadra1 = dfcopy.loc[0, 'team1']
      squadra2 = dfcopy.loc[0, 'team2']

      rows_index = dfcopy.index[(dfcopy['team1'] == squadra1) &
                                (dfcopy['team2'] == squadra2)].tolist()
      
      if(len(rows_index) > 0):
         for i in range(len(rows_index) - 1):
            first = dfcopy.iloc[rows_index[i]]
            second = dfcopy.iloc[rows_index[i+1]]
            found = False

            if(first['origin'] != second['origin']):
               if(first['1'] > 2 and second['X2'] > 2):
                  found = True
               if(first['2'] > 2 and second['1X'] > 2):
                  found = True
               if(first['X'] > 2 and second['12'] > 2):
                  found = True
               if(first['gol si'] > 2 and second['gol no'] > 2):
                  found = True
               if(first['gol no'] > 2 and second['gol si'] > 2):
                  found = True   

               if(found == True):
                  print(first)
                  print(second)   
      else:
         pass

      dfcopy = dfcopy.drop(rows_index)
      #print(dfcopy)
      if(len(dfcopy) > 0):
         dfcopy = dfcopy.reset_index(drop = True)
   

'''
allPages = ["https://sports.bwin.it/it/sports/calcio-4/scommesse/italia-20",
            "https://www.sisal.it/scommesse-matchpoint/quote/calcio/serie-a",
         ]
'''
allPages = ["https://sports-bwin-it.translate.goog/it/sports/calcio-4/scommesse/italia-20?_x_tr_sl=auto&_x_tr_tl=en&_x_tr_hl=en-US&_x_tr_pto=wapp&_x_tr_hist=true"]



def main():
   print(dataFrame)
   dizionarioPagine = Pagine()   
   driver = webdriver.Edge()
   driver.set_window_size(4000,2000)
   
   driver.get(allPages[0])
   driver.fullscreen_window()
   driver.execute_script("document.body.style.zoom='75%'")

   dizionarioPagine.add('primo', driver.current_window_handle)
   '''
   driver.execute_script("window.open('about:blank', 'secondtab');")
   driver.switch_to.window("secondtab")

   dizionarioPagine.add('secondo', driver.current_window_handle)
   
   driver.get(allPages[1])
   driver.fullscreen_window()
   driver.execute_script("document.body.style.zoom='75%'")
   '''
   wait = WebDriverWait(driver, 10)
   #element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "sort-toggle-button left-btn active")))
   
   #time.sleep(10)
   
   
   driver.switch_to.window(dizionarioPagine.getUrlWithGivenDescription("primo"))
   driver.set_window_size(4000,2000)      #?????????
   driver.fullscreen_window()
   driver.execute_script("document.body.style.zoom='75%'")
   time.sleep(1)

   while(True):
      time.sleep(2)
      os.system('cls')
      getBwin(driver)
      print(dataFrame)
   

   '''
   driver.switch_to.window(dizionarioPagine.getUrlWithGivenDescription("secondo"))
   driver.set_window_size(4000,2000)
   driver.fullscreen_window()
   driver.execute_script("document.body.style.zoom='75%'")
   time.sleep(10)

   while(True):
      time.sleep(2)
      os.system('cls')
      getSisal(driver)
      checkOpportunity()
      print(dataFrame)
   '''

   while(True):
      driver.switch_to.window(dizionarioPagine.getUrlWithGivenDescription("primo"))
      driver.fullscreen_window()
      driver.execute_script("document.body.style.zoom='75%'")
      time.sleep(1)
      getBwin(driver)

      driver.switch_to.window(dizionarioPagine.getUrlWithGivenDescription("secondo"))
      driver.fullscreen_window()
      driver.execute_script("document.body.style.zoom='75%'")
      time.sleep(1)
      getSisal(driver)

      os.system('cls')
      print(dataFrame)
      checkOpportunity()
      
      



   time.sleep(10)
      
   

def testFunction():
   checkOpportunity()

if __name__ == "__main__":
   main()
   #testFunction()
   
   