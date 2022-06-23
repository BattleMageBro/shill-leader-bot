from aiogram.utils.helper import Helper, HelperMode, ListItem


class BotStates(Helper):
    mode = HelperMode.snake_case
    
    #PENDING == None for neutral state
    PENDING = ListItem()

    #Shilling states
    START_SHILLING = ListItem()
    SHILLING = ListItem()
    END_SHILLING = ListItem()

    #Add options for shilling
    CHOOSE_CHAT = ListItem()
    CHOOSE_SHILL_MESSAGE = ListItem()
    CHOOSE_SHILL_MESSAGE_OPTS = ListItem()
    CHOOSE_TIMEOUT = ListItem()
    CHOOSE_LINKS = ListItem()
    CHOOSE_LINKS_OPTS = ListItem()

    TEST_STATE_5 = ListItem()