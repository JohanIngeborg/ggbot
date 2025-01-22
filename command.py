from selenium.webdriver.common.by import By
from utils.utilities import filterBmp, clearChat, waitFindInputAndSendKeys
from datetime import date
from datetime import datetime

class Command:

    # List of all commands and their descriptions, to use in help command
    command_type_list = []
    driver = None
    

    def __init__(self, driver, command_name, description, is_text_after_command : bool):

        Command.driver = driver
        self.command_name = command_name
        self.description = description
        self.is_text_after_command = is_text_after_command
        # List of last command uses in the chat before clearing it, just for temporary use

        # add command name and description to use it in /help
        Command.command_type_list.append(f"/{command_name} - {description}")


    def __commandXpath(self):
        xpath = ""

        if(self.is_text_after_command == True):

            xpath = ( #image generation command
            "//*[@class='ml__item-part-content' " # command is in the active chat
            f"and starts-with(normalize-space(text()), '/{self.command_name} ') " # command starts with '/binguj '
            f"and string-length(normalize-space(text())) > string-length('/{self.command_name} ')]" # command is not empty after '/binguj '
            )

        # for commands like '/restart' which don't need additional input
        else:
            xpath = (
            "//*[@class='ml__item-part-content' "
            f"and normalize-space(text())='/{self.command_name}']"
            )
        
        # make list of all command names and it description to use it in /help                

        return xpath
    

    # Find the nickname of the user who sent the command. If someone wrote multiple messages in a row, 
    # find their first message to get the element with the nickname.
    def get_commands_data(self):

        received_commands = [] # list of all commands found in the chat before clearing it
        command_data = {} # data of a single command

        # Only incoming messages, so the bot can ignore itself (outgoing messages)
        incoming_messages = self.driver.find_elements(By.CLASS_NAME, "ml__item--incoming")
        is_command_found = False

        if incoming_messages:

            input = ""
            user_nickname = ""
            time = {}

            for message in reversed(incoming_messages):

                print(f"Znaleziono: {len(incoming_messages)} wiadomości")
                # xpath to find specific commands in the chat
                xpath = self.__commandXpath()
                raw_command_elements = message.find_elements(By.XPATH, f".{xpath}")  # Wait until the command is found and make a list of them

                # Check if the user has sent a command and turn on a switch to look for the user's nickname
                if raw_command_elements:
                    print(f"Message: {raw_command_elements[0].text}, remove: {self.command_name}")
                    
                    # use lstrip to remove command name and whitespaces from the start of the text
                    input = raw_command_elements[0].text.lstrip(f"/{self.command_name}")
                    input = input.strip()  # remove whitespaces from the start and end of the text
                    input = filterBmp(input)  # Filter out unsupported characters from the text

                    is_command_found = True

                # Look for the nickname only if the user sent a command
                if is_command_found:
                    nickname_elements = message.find_elements(By.CLASS_NAME, "ml__item-username")
                    print(f"Nick found: {len(nickname_elements)}")

                    if nickname_elements:
                        print(f"Nick: {nickname_elements[0].text}")

                        # Extract and clean the nickname
                        user_nickname = nickname_elements[0].text
                        user_nickname = filterBmp(user_nickname)


                        # Add command info to the dictionary
                        command_data["user"] = user_nickname
                        command_data["command"] = self.command_name
                        command_data["input"] = input

                        time["hour"] = datetime.now().hour
                        time["minute"] = datetime.now().minute
                        time["day"] = datetime.now().day
                        time["month"] = datetime.now().month
                        time["year"] = datetime.now().year

                        command_data["time"] = time

                        received_commands.append(command_data)
                        print(command_data)

                        # Reset the command-found flag for the next iteration
                        is_command_found = False
                
                

        # it should return a list of dictionaries containing all information about the command - input, nickname, date    
        return received_commands
    
    
    # display a list of all commands and their descriptions
    @staticmethod
    def help():
        for line in Command.command_type_list:
            waitFindInputAndSendKeys(Command.driver, 1, By.ID, "chat-text", line)
