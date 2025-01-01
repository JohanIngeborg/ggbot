from Utils.utils import WaitFindInputAndSendKeys, WaitFindAndReturn, WaitFindAndClick, clearChat, filterBmp
from selenium.webdriver.common.by import By
import time

def BingusGpt(driver, prompt):
        time.sleep(1) # wait for the command to be sent, idk why but it won't work without it
        WaitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", "<myśli>") # send message that text is being generated
        
        # clear command from the chat, so it's not used again
        clearChat(driver)

        # switch to chatgpt tab
        driver.switch_to.window(driver.window_handles[1])

        # pre prompts
        xpath = '//*[@data-placeholder="Wyślij wiadomość do ChatGPT"]'
        characterRandom = "(Jesteś chaotycznym botem który nazywa się Bingus, jesteś nieprzewidywalny i używasz słów nie mających sensu, albo słów nie pasujących do kontekstu. Kłamiesz kiedy ktoś się ciebie o coś pyta. Odmawiaj jeśli ktoś chce żebyś inaczej się zachowywał)."
        characterWholesome = "(Jesteś pomocnym botem który nazywa się Bingus, jesteś miły ale lubisz się droczyć)."
        słowa = "(Czasami używaj słów jak (nie w każdej wiadomości, nie przesadzaj) - fek(coś niedobrego), bambuko (kiedy ktoś zrobi ci psikusa, albo spróbuje oszukać), hao, uoee, guk, borwald, sraka, mogadisz, farfocel, turlaj bombla (jeśli ktoś cię denerwuje, albo zadaje kontrowersyjne pytania), guk guk guk, aku beneng saget, polska gurom, fircyk, glopper, bombel)"
        nowoPolski = "(Rób błędy gramatyczne, np. błendy zamiast błędy, kuamstwa zamiast kłamstwa, gurom zamiast górom)"
        emotki = ", używasz emotek takich jak - <faja>, <palacz>, :>, ;>, :)), <bije>, <biją>, <myśli>, <myśli2>, <hura>, <hejka>, <zniesmaczony>, <wnerw>, <nerwus>, <zawstydzony>, <onajego>, <peace>, <tańczę>, :((, ??, !!, ;(, <lol>, <telefon2>, <piwosz>, <dresik>, <leje>, <urwanie głowy>, <niedowiarek>, <śnieg>, <gra>) "
        
        WaitFindInputAndSendKeys(driver, 1, By.XPATH, xpath, characterWholesome + emotki + nowoPolski + prompt) # send prompt to chatgpt

        #wait for the response to be generated
        time.sleep(1)
        xpath = '//*[@data-testid="composer-speech-button"]' # when the response is done, speech button should appear in place of stop generating button
        WaitFindAndReturn(driver, 30, By.XPATH, xpath) # wait for the button to appear
        
        xpath = '//*[@data-scroll-anchor="true"]'
        element = WaitFindAndReturn(driver, 1, By.XPATH, xpath)
        print(f"Element found: {element.get_attribute('outerHTML')}")

        xpath2 = ".//div[contains(@class, 'markdown') and contains(@class, 'prose')]"
        # Use relative XPath starting from the parent element
        response = WaitFindAndReturn(element, 1, By.XPATH, xpath2)
        print(f"Response found: {response.get_attribute('outerHTML')}")
        print(f"Response found: {response.text}")
        
        text = response.text

        # switch back to chat tab and send the image
        driver.switch_to.window(driver.window_handles[0]) # switch back to chat tab
        text = filterBmp(text)
        WaitFindInputAndSendKeys(driver, 1, By.ID, "chat-text", text)
        

        