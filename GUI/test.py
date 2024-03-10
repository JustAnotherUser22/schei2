import pyautogui
import time


#leggi questo se non trovi qualcosa
#https://stackoverflow.com/questions/45302681/running-pyautogui-on-a-different-computer-with-different-resolution


def main():
   time.sleep(5)
   #im1 = pyautogui.screenshot()
   #im2 = pyautogui.screenshot('my_screenshot.png')
   print('end')

   button7location = pyautogui.locateOnScreen('digit7.png', grayscale = False)
   time.sleep(5)
   button7point = pyautogui.center(button7location)
   button7x, button7y = button7point
   pyautogui.click(button7x, button7y)  # clicks the center of where the 7 button was found
   #pyautogui.click('calc7key.png') # a shortcut version to click on the center of where the 7 button was found


def mouse():
   print(pyautogui.size())
   
   pyautogui.moveTo(1920-10, 1080-10, duration = 3)
   #pyautogui.moveTo(1920/2+100, 1080/2, duration = 3)




if __name__ == "__main__":
   #main()
   mouse()