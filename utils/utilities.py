from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

##functions
# find element by type and wait until it is clickable
def waitFindAndClick(context, waitTime, by, elementName):
    # for attempt in range(3):  # Retry up to 3 times
    #     try:
            # Wait until the element is clickable
    WebDriverWait(context, waitTime + 10).until(
        EC.element_to_be_clickable((by, elementName))
    )
    # Locate and click the element
    element = context.find_element(by, elementName)
    element.click()
            # return  # Exit the function if successful
    #     except StaleElementReferenceException:
    #         print(f"Attempt {attempt + 1}: Element became stale, retrying...")
    #         continue  # Retry by re-locating the element
    # # If all attempts fail, raise an exception
    # raise Exception(f"Could not interact with the element {elementName} after 3 attempts.")
        

# wait until input bar has loaded, look for it and send text with ENTER
def waitFindInputAndSendKeys(context, waitTime, by, elementName, inputText):
    # for attempt in range(3):  # Retry up to 3 times
    #     try:
            # Wait for the element to be present
    WebDriverWait(context, waitTime + 10).until(
        EC.presence_of_element_located((by, elementName))
    )
    # Find and interact with the element
    element = context.find_element(by, elementName)
    element.clear()
    element.send_keys(inputText + Keys.ENTER)


    #         return  # Exit the function if successful
    #     except StaleElementReferenceException:
    #         # Log a message or retry finding the element
    #         print(f"Attempt {attempt + 1}: Element became stale, retrying...")
    #         continue
    # # If all attempts fail, raise the exception
    # raise Exception(f"Could not interact with the element {elementName} after 3 attempts.")


# find element by type and return it
def waitFindAndReturn(context, waitTime, by, elementName):
    WebDriverWait(context, waitTime + 10).until(
        EC.presence_of_element_located((by, elementName))
    )
    element = context.find_element(by, elementName)
    return element

def filterBmp(text):
    return ''.join(c for c in text if ord(c) <= 0xFFFF)

def clearChat(driver):
    toolbar = waitFindAndReturn(driver, 1, By.CLASS_NAME, "toolbar-right") # find chat toolbar
    waitFindAndClick(toolbar, 1, By.CLASS_NAME, "settings-btn") # click on settings button
    waitFindAndClick(driver, 1, By.CLASS_NAME, "clear-all") # click on clear all messages