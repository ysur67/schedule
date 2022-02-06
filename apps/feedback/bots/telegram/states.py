from aiogram.utils.helper import Helper, HelperMode, ListItem


class UserStates(Helper):
    mode = HelperMode.snake_case

    CHOOSE_GROUP_STATE = ListItem()
    CHANGE_SETTINGS_STATE = ListItem()
    CHANGE_DAYS_OFFSET_STATE = ListItem()
