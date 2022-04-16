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
    CHOOSE_SHILL_MESSAGES = ListItem()
    CHOOSE_TIMEOUT = ListItem()
    CHOOSE_LINKS = ListItem()

    TEST_STATE_5 = ListItem()