from enum import Enum

from telegram import BotCommand


class Commands(Enum):
    ADD_RESTAURANT = "افزودن رستوران"
    ACTIVE_RESTAURANT = "رستوران های فعال"
    REMOVE_RESTAURANT = "حذف رستوران"
    CHANGE_BOT_RUNNING_STATUS = "شروع/توقف تخفیف یاب"
    BACK_TO_MAIN_MENU = "بازگشت به منوی اصلی"

commands = [
    BotCommand('start', 'شروع ربات'),
    BotCommand('cancel', 'خروج به منوی اصلی')
]