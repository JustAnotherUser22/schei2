import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dizionarioPagine import *
import time

def main():
   dizionarioPagine = Pagine()   
   driver = webdriver.Chrome()
   lastText = ''
   lastText2 = ''

   driver.get("https://www.oraesatta.co/")
   wait = WebDriverWait(driver, 10)
   element = wait.until(EC.element_to_be_clickable((By.ID, "clock")))
   clock = driver.find_element(By.ID, "clock")

   dizionarioPagine.add('primo', driver.current_window_handle)
   
   driver.execute_script("window.open('about:blank', 'secondtab');")
   driver.switch_to.window("secondtab")

   dizionarioPagine.add('secondo', driver.current_window_handle)
   
   driver.get("https://www.oraesattaitalia.it/")
   wait = WebDriverWait(driver, 10)
   element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "jumbotron")))
   clock2 = driver.find_element(By.CLASS_NAME, "jumbotron")

   
   while(True):
      time.sleep(2)
      driver.switch_to.window(dizionarioPagine.getUrlWithGivenDescription("primo"))
      string = clock.text
      hour = string.split('\n')[0]
      if(hour != lastText):
         lastText = hour
         print("1: {0}".format(lastText))
      
      driver.switch_to.window(dizionarioPagine.getUrlWithGivenDescription("secondo"))
      string = clock2.text
      hour = string.split('\n')[0]
      if(hour != lastText2):
         lastText2 = hour
         print("2: {0}".format(lastText2))
      
   

if __name__ == "__main__":
   main()
   
   