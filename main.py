from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput import keyboard
import time
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException
from Utils.utils import WaitFindInputAndSendKeys, WaitFindAndReturn, WaitFindAndClick
from binguj import Binguj

# setup chrome profile, so it doesn't ask for logins
chrome_options = Options()
chrome_options.add_argument("user-data-dir=C:/Users/gordi/AppData/Local/Google/Chrome/User Data")  # Path to your profile
chrome_options.add_argument("--profile-directory=Default")  # Default profile directory

# setup chrome driver
try:
    service = Service(executable_path='chromedriver.exe', service_args=["--verbose", "--log-path=chromedriver.log"])
    driver = webdriver.Chrome(service=service, options=chrome_options)
except Exception as e:
    print(f"Error initializing the Chrome driver: {e}")    
    exit(1)

# prepare tabs before starting bot operations
driver.get('https://www.gg.pl/#latest') # open webgg page
driver.maximize_window()

chatName = 'Ing'
try:
    WaitFindAndClick(driver, 10, By.XPATH, f"//*[text()='Ing']") # click on profile and start chat, avoid stale element exception
except StaleElementReferenceException:
    WaitFindAndClick(driver, 10, By.XPATH, f"//*[text()='Ing']")

WaitFindAndClick(driver, 10, By.CLASS_NAME, "talk-button")  # click on talk button to start chat
driver.execute_script("window.open('https://www.bing.com/images/create');") # open bing ai on new tab and return to chat tab
driver.switch_to.window(driver.window_handles[0]) # switch to chat tab (0)

# main loop for bot operations
while(True):    
    # for testing purposes automatically send command
    # WaitFindInputAndSendKeys(driver, 5, By.ID, "chat-text", "/binguj gf fdfd")
    # time.sleep(1) # wait for the command to be sent
    
    # find command in the chat
    bingujCommand = (
        "//*[@class='ml__item-part-content' " #check if command is in the active chat
        "and starts-with(normalize-space(text()), '/binguj ') " #check if command starts with '/binguj '
        "and string-length(normalize-space(text())) > string-length('/binguj ')]" #check if command is not empty after '/binguj '
    )
    
    commands = driver.find_elements(By.XPATH, bingujCommand) # wait until command is found and make list of them
    commandTextList = [command.text.replace("/binguj ", "") for command in commands] if commands else [] # process commands from the list into a list of strings, which can be used as prompts

    # if command is found
    if commandTextList:
        try:
            for commandText in commandTextList:
                Binguj(driver, commandText) # call Binguj function with the command as an argument
        
        except TimeoutException:
            print("Error while executing Binguj function")
            driver.switch_to.window(driver.window_handles[0])
            WaitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", f"Nie udało się wybingować {commandText} ;(")
            continue

driver.quit()