from enum import Enum

class Commands(Enum):
    ADD_RESTAURANT = "افزودن رستوران"
    ACTIVE_RESTAURANT = "رستوران های فعال"
    REMOVE_RESTAURANT = "حذف رستوران"
    CHANGE_BOT_RUNNING_STATUS = "شروع/توقف تخفیف یاب"
    BACK_TO_MAIN_MENU = "بازگشت به منوی اصلی"