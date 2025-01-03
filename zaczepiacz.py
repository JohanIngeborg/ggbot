from Utils.utils import WaitFindInputAndSendKeys, WaitFindAndReturn, WaitFindAndClick, clearChat, filterBmp
from selenium.webdriver.common.by import By
from bingusGpt import GetAnswerAndSendItOnChat

import time

def Zaczepiacz(driver, prompt):
    time.sleep(1) # wait for the command to be sent, idk why but it won't work without it
    clearChat(driver) # clear messages from the chat, so it's not used again

    # switch to chatgpt tab, so we can send the prompt and generate the response
    driver.switch_to.window(driver.window_handles[1])
    emotki = "(używasz emotek takich jak - <faja>, <palacz>, :>, ;>, :)), <bije>, <biją>, <myśli>, <myśli2>, <hura>, <hejka>, <zniesmaczony>, <wnerw>, <nerwus>, <zawstydzony>, <onajego>, <peace>, <tańczę>, :((, ??, !!, ;(, <lol>, <telefon2>, <piwosz>, <dresik>, <leje>, <urwanie głowy>, <niedowiarek>, <śnieg>, <gra>) "
    # prompt = "Napisz prostą zaczepkę do jednej osoby z grona (Ing, Zefir, Tadeusz, Garett, Marcin)"

    GetAnswerAndSendItOnChat(driver, emotki + prompt)

