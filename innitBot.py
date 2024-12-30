from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from Utils.utils import WaitFindInputAndSendKeys, WaitFindAndReturn, WaitFindAndClick, clearChat

def InitBot(driver):
    # Close all tabs except the first one to perform a clean start
    main_tab = driver.window_handles[0]  # Store the first tab
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if handle != main_tab:
            driver.close()

    # Switch back to the first tab
    driver.switch_to.window(main_tab)

    # open tabs and prepare them for bot operations
    driver.get('https://www.gg.pl/#latest') # open webgg page
    driver.maximize_window()

    chatKomfa = 'Komfa'
    chatIng = 'Ing' # test chat

    WaitFindAndClick(driver, 1, By.XPATH, f"//*[text()='{chatIng}']") # click on profile and start chat, avoid stale element exception
    WaitFindAndClick(driver, 1, By.CLASS_NAME, "talk-button")  # click on talk button to start chat

    driver.execute_script("window.open('https://www.bing.com/images/create');") # open bing ai on new tab and return to chat tab
    driver.execute_script("window.open('https://chatgpt.com/');") # open chatgpt on new tab and return to chat tab

    driver.switch_to.window(driver.window_handles[0]) # switch to chat tab and wait for commands

    WaitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", "Jestem gotowy! <bije>") # send message that bot is ready