from aiogram.utils.helper import Helper, HelperMode, ListItem


class TestStates(Helper):
    mode = HelperMode.snake_case

    PENDING = ListItem()
    START_SHILLING = ListItem()
    CHOOSE_SHILL_OPTS = ListItem()
    SHILLING = ListItem()
    END_SHILLING = ListItem()
    TEST_STATE_5 = ListItem()
    def __init__(self, chat_id):
        self.chat_id = chat_id
