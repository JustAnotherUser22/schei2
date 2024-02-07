import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from dizionarioPagine import *
from selenium.webdriver.support.ui import Select


def waitTillMainPageIsReady(driver):
   XPATH_BUTTON_LANGUAGE = '//*[@id="root"]/div[1]/nav/div[3]/ul/li[6]'
   wait = WebDriverWait(driver, 10)
   element = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BUTTON_LANGUAGE)))
   


def insertPassword(driver):
   XPATH_BUTTON_VISUALIZZAZIONE = '//*[@id="root"]/div[1]/nav/div[3]/ul/li[5]/span/span'
   XPATH_PANEL_INSERIMENTO_PASSWORD = '//*[@id="idKeyboardInput"]'
   XPATH_BUTTON_CONFERMA = '/html/body/div[1]/div[1]/div[3]/div[4]/button[1]/span'

   #buttonVisualizzazione = driver.find_element(By.CSS_SELECTOR, ".main-nav__base.main-nav__userlevel.nav-item")
   buttonVisualizzazione = driver.find_element(By.XPATH, XPATH_BUTTON_VISUALIZZAZIONE)
   buttonVisualizzazione.click()

   #pwdField = driver.find_element(By.ID, "idKeyboardInput")
   pwdField = driver.find_element(By.XPATH, XPATH_PANEL_INSERIMENTO_PASSWORD)
   pwdField.click()
   pwdField.send_keys("222222")

   conferma = driver.find_element(By.CLASS_NAME, "panel-input__text")
   #conferma = driver.find_element(By.XPATH, XPATH_BUTTON_CONFERMA)
   #conferma = driver.find_element(By.LINK_TEXT, "Conferma")
   allButtons = driver.find_elements(By.TAG_NAME, 'button')
   for button in allButtons:
      if(button.text == "CONFIRM"):
         button.click()
         break

   #conferma.click()

def changeLanguage(driver):
   XPATH_BUTTON_LANGUAGE = '//*[@id="root"]/div[1]/nav/div[3]/ul/li[6]'

   button = driver.find_element(By.XPATH, XPATH_BUTTON_LANGUAGE)
   button.click()

   #time.sleep(2)
   wait = WebDriverWait(driver, 10)
   element = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.language-selector__modal-body-item.list-group-item')))

   allPossibleLanguages = driver.find_elements(By.CSS_SELECTOR, '.language-selector__modal-body-item.list-group-item')
   for entry in allPossibleLanguages:
      if(entry.text == 'Italiano' or entry.text == 'Italian'):
         entry.find_element(By.CLASS_NAME, 'checkmarkround').click()
         break
   


def queryAll(driver):

   XPATH_BUTTON_FUNZIONI = "//*[@id='root']/div[1]/div/div[2]/ul/li[5]/a/span/span"
   XPATH_BUTTON_AGGIORNAMENTO_FIRMWARE = "//*[@id='root']/div[1]/div/div[2]/ul[2]/li[2]/a/span"
   XPATH_BUTTON_QUERY_DEVICE = "//*[@id='root']/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[1]/button[1]"
   XPATH_SELECT_CHOOSE = "//*[@id='id_teleload__combo']"
   XPATH_BUTTON_NEXT = '//*[@id="root"]/div[1]/div/div[1]/div/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/div/div[2]/div[2]/button'

   funzioni = driver.find_element(By.XPATH, XPATH_BUTTON_FUNZIONI)
   funzioni.click()

   aggiornamento = driver.find_element(By.XPATH, XPATH_BUTTON_AGGIORNAMENTO_FIRMWARE)
   aggiornamento.click()

   queryDevice = driver.find_element(By.XPATH, XPATH_BUTTON_QUERY_DEVICE)
   queryDevice.click()

   choose = driver.find_element(By.XPATH, XPATH_SELECT_CHOOSE)
 
   select = Select(choose)
   select.select_by_visible_text("ALL")

   next = driver.find_element(By.XPATH, XPATH_BUTTON_NEXT)
   next.click()

   



def openPage():
   dizionarioPagine = Pagine()
   driver = webdriver.Chrome()
   driver.get("http://serverovpn.saviotechnologies.com:81/#/machines_overview")
   driver.fullscreen_window()
   
   dizionarioPagine.add('primo', driver.current_window_handle)

   #time.sleep(2)
   wait = WebDriverWait(driver, 10)
   element = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, 'LOEPFE')))

   buttonSavio = driver.find_element(By.LINK_TEXT, "SAVIO")
   buttonSavio.click()

   buttonSalaProve = driver.find_element(By.LINK_TEXT, "SALA PROVE")
   buttonSalaProve.click()

   buttonMacchina = driver.find_element(By.LINK_TEXT, "10.139.170.74")
   buttonMacchina.click()

   #qui apre una nuova pagina
   for handle in driver.window_handles:
      if(dizionarioPagine.IsPathInDictionary(handle) == False):
         dizionarioPagine.add('secondo', handle)

   driver.switch_to.window(dizionarioPagine.getUrlWithGivenDescription("secondo"))
   driver.fullscreen_window()

   wait = WebDriverWait(driver, 10)
   #element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Funzioni')))
   element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div[1]/nav/div[3]/ul/li[5]/span/span")))
   
   insertPassword(driver)
   queryAll(driver)  



def openPwd():
   driver = webdriver.Edge()
   driver.get("http://10.139.170.74")
   driver.fullscreen_window()

   wait = WebDriverWait(driver, 10)
   #element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, 'Funzioni')))
   element = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div[1]/nav/div[3]/ul/li[5]/span/span")))
   
   insertPassword(driver)
   changeLanguage(driver)
   waitTillMainPageIsReady(driver)
   queryAll(driver)

   time.sleep(10)





if __name__ == "__main__":
   #openPage()
   openPwd()