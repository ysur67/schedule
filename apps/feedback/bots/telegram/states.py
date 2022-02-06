from aiogram.utils.helper import Helper, HelperMode, Item


class UserStates(Helper):
    mode = HelperMode.snake_case

    CHOOSE_GROUP_STATE = Item()
    CHANGE_SETTINGS_STATE = Item()
    CHANGE_DAYS_OFFSET_STATE = Item()
