from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException, WebDriverException
from Utils.utils import WaitFindInputAndSendKeys, WaitFindAndReturn, WaitFindAndClick, clearChat
from binguj import Binguj
from innitBot import InitBot

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

# initialize bot
InitBot(driver)

# main loop for bot operations
while(True):
    # for testing purposes automatically send command
    # WaitFindInputAndSendKeys(driver, 5, By.ID, "chat-text", "/binguj gf fdfd")
    # time.sleep(1) # wait for the command to be sent
    
    # find command in the chat
    bingujCommand = ( #image generation command
        "//*[@class='ml__item-part-content' " #check if command is in the active chat
        "and starts-with(normalize-space(text()), '/binguj ') " #check if command starts with '/binguj '
        "and string-length(normalize-space(text())) > string-length('/binguj ')]" #check if command is not empty after '/binguj '
    )

    # bingusCommand = ( # chatgpt command
    #     "//*[@class='ml__item-part-content' " #check if command is in the active chat
    #     "and starts-with(normalize-space(text()), 'Bingus') " #check if command starts with '/binguj '
    #     "and string-length(normalize-space(text())) > string-length('Bingus ')]" #check if command is not empty after '/binguj '
    # )
    restartXPATH = (
        "//*[@class='ml__item-part-content' "
        "and normalize-space(text())='/restart']"
    )
    
    commands = driver.find_elements(By.XPATH, bingujCommand) # wait until command is found and make list of them
    commandTextList = [command.text.replace("/binguj ", "") for command in commands] if commands else [] # process commands from the list into a list of strings, which can be used as prompts
    restartCommand = driver.find_elements(By.XPATH, restartXPATH) # check if restart command is in the chat
    
    # if command is found
    if commands:
        for commandText in commandTextList:
            try:
                Binguj(driver, commandText)  # Call Binguj function with the command as an argument
            except TimeoutException:
                print("Timeout occurred while executing Binguj function")
                driver.switch_to.window(driver.window_handles[0])
                safe_text = commandText if isinstance(commandText, str) else str(commandText)
                WaitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", f"Nie udało się wybingować {safe_text} ;(")
                continue
            except WebDriverException as e:
                if "ChromeDriver only supports characters in the BMP" in str(e):
                    print(f"Unsupported characters detected in: {commandText}")
                    WaitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", f"Niedozwolone znaki <zniesmaczony>")
                    clearChat(driver)
                else:
                    print(f"WebDriverException: {e}")
                driver.switch_to.window(driver.window_handles[0])
                continue
            except Exception as e:
                print(f"Unexpected error: {type(e).__name__}, {e}")
                driver.switch_to.window(driver.window_handles[0])
                continue
    #restart a bot
    elif restartCommand:
        WaitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", "Restartuje się <palacz>")
        clearChat(driver)
        InitBot(driver)


driver.quit()