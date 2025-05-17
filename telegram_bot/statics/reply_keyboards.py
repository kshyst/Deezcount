from telegram import KeyboardButton

from telegram_bot.statics.commands import Commands

add_restaurant_button = KeyboardButton(
    text=Commands.ADD_RESTAURANT.value,
)
active_restaurant_button = KeyboardButton(
    text=Commands.ACTIVE_RESTAURANT.value,
)
remove_restaurant_button = KeyboardButton(
    text=Commands.REMOVE_RESTAURANT.value,
)
change_bot_status_button = KeyboardButton(
    text=Commands.CHANGE_BOT_RUNNING_STATUS.value,
)
back_to_main_menu_button = KeyboardButton(
    text=Commands.BACK_TO_MAIN_MENU.value
)

main_menu_buttons = [
    [add_restaurant_button, active_restaurant_button],
    [remove_restaurant_button, change_bot_status_button],
]

in_menu_buttons = [
    [back_to_main_menu_button],
]