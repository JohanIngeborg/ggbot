from Utils.utils import WaitFindInputAndSendKeys, WaitFindAndReturn, WaitFindAndClick
from selenium.webdriver.common.by import By
import time

def Binguj(driver, commandText):
    time.sleep(1) # wait for the command to be sent, idk why but it won't work without it
    WaitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", f"Binguje obraz {commandText} <faja>") # send message that image is being generated

    # clear command from the chat, so it's not used again
    toolbar = WaitFindAndReturn(driver, 1, By.CLASS_NAME, "toolbar-right") # find chat toolbar
    WaitFindAndClick(toolbar, 1, By.CLASS_NAME, "settings-btn") # click on settings button
    WaitFindAndClick(driver, 1, By.CLASS_NAME, "clear-all") # click on clear all messages

    # switch to bing tab
    driver.switch_to.window(driver.window_handles[1]) 

    # wait until bing ai searchbox has loaded and look for it to send a prompt
    WaitFindInputAndSendKeys(driver, 1, By.CLASS_NAME, "b_searchbox", commandText)     
    WaitFindAndClick(driver, 240, By.CLASS_NAME, "imgri-container") # click on generated image to open Iframe
    print("Image generated")

    # switch to iframe with generated image
    iframe = WaitFindAndReturn(driver, 1, By.XPATH, "//iframe[@id='OverlayIFrame']")
    driver.switch_to.frame(iframe)

    # find element with generted image
    generatedImage = (
        f"//*[(@role='button') and (@aria-label='{commandText}')]" # look for button with aria label equal to prompt
    )
    imgElement = WaitFindAndReturn(driver, 1, By.XPATH, generatedImage)
    imageSrc = imgElement.get_attribute("src")
    # print(f"Element found: {imgElement[0].get_attribute("outerHTML")}")
    if imageSrc:
        print("Image found: " + imageSrc)
    else:
        print("Image src attribute is None")

    # cleanup bing tab
    WaitFindAndClick(driver, 1, By.XPATH, "//*[(@data-tooltip='Zamknij obraz')]") # close image Iframe
    driver.switch_to.default_content() # Exit iframe and switch back to the main document

    # switch back to chat tab and send the image
    driver.switch_to.window(driver.window_handles[0]) # switch back to chat tab
    if imageSrc is None:
        chatMsg = "Nie udało się wygenerować obrazu"
    else:
        chatMsg = imageSrc
    WaitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", chatMsg)