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
    CHOOSE_PACK_OR_SELF = ListItem()
    CHOOSE_PACKS = ListItem()
    CHOOSE_PACKS_OPTS = ListItem()
    CHOOSE_LINKS = ListItem()
    CHOOSE_LINKS_OPTS = ListItem()
    CHOOSE_SHILL_MESSAGE = ListItem()
    CHOOSE_SHILL_MESSAGE_OPTS = ListItem()
    CHOOSE_TIMEOUT = ListItem()
    CHOOSE_TIMEOUT_OPTS = ListItem()
    CHOOSE_SHILL_END = ListItem()
