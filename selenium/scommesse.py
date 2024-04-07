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
from strutturaDati import *


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
   
   