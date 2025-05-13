from telegram import KeyboardButton

from telegram_bot.statics.commands import Commands

add_restaurant_button = KeyboardButton(
    text=Commands.ADD_RESTAURANT.value,
)
active_restaurant_button = KeyboardButton(
    text=Commands.ACTIVE_RESTAURANT.value,
)

main_menu_buttons = [
    [add_restaurant_button, active_restaurant_button],
]