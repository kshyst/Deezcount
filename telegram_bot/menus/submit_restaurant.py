from asgiref.sync import sync_to_async
from telegram import (
    Update,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from telegram_bot import get_restaurant_list
from telegram_bot.statics.menu_ranges import RESTAURANT_NAME, SELECT_RESTAURANT, ENTRY
from telegram_bot.statics.reply_keyboards import in_menu_buttons
from telegram_user.models import AvailableRestaurant, ActiveRestaurant, User


async def send_restaurant_search_query(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="نام رستوران مورد نظر خود را وارد کنید.",
        reply_to_message_id=update.effective_message.id,
        reply_markup=ReplyKeyboardMarkup(
            in_menu_buttons, one_time_keyboard=True
        ),
    )
    return RESTAURANT_NAME

async def show_restaurant_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    search_query = update.message.text
    restaurant_list = get_restaurant_list(search_query)
    context.user_data['restaurant_list'] = restaurant_list

    if not restaurant_list:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="رستورانی با این نام پیدا نشد. لطفا دوباره تلاش کنید.",
            reply_to_message_id=update.effective_message.id,
        )
        return RESTAURANT_NAME
    else:
        message = "رستوران های پیدا شده:\n"

        for restaurant in restaurant_list:
            num = restaurant.get("number")
            title = restaurant.get("title")
            message += f"{num} - {title}\n\n"

        message += "لطفا شماره رستوران مورد نظر خود را ارسال کنید."

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
        )
        return SELECT_RESTAURANT

async def select_restaurant(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    restaurant_num = update.message.text

    try:
        restaurant_num = int(restaurant_num)
    except ValueError:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="لطفا یک شماره وارد کنید.",
            reply_to_message_id=update.effective_message.id,
        )
        return SELECT_RESTAURANT

    if restaurant_num not in range(1, len(context.user_data['restaurant_list']) + 1):
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="لطفا یک شماره معتبر وارد کنید.",
            reply_to_message_id=update.effective_message.id,
        )
        return SELECT_RESTAURANT

    # ger res data
    restaurant = context.user_data['restaurant_list'][restaurant_num - 1]
    restaurant_name = restaurant.get("title")
    restaurant_code = restaurant.get("code")

    # save the res to the database
    if not await sync_to_async(AvailableRestaurant.objects.filter(restaurant_code=restaurant_code).exists)():
        restaurant_object = AvailableRestaurant(restaurant_name=restaurant_name, restaurant_code=restaurant_code)
        await sync_to_async(restaurant_object.save)()

        restaurant_active_object = ActiveRestaurant(restaurant=restaurant_object)
        await sync_to_async(restaurant_active_object.save)()
    else:
        restaurant_object = await sync_to_async(AvailableRestaurant.objects.get)(restaurant_code=restaurant_code)
        restaurant_active_object = await sync_to_async(ActiveRestaurant.objects.get)(restaurant=restaurant_object)

    # add the res for the user
    user = await sync_to_async(User.objects.get)(telegram_id=update.effective_chat.id)
    await sync_to_async(user.restaurant.add)(restaurant_active_object)
    await sync_to_async((await sync_to_async(User.objects.get)(telegram_id=update.effective_chat.id)).save)()

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"شما رستوران {restaurant_name} را انتخاب کردید.",
        reply_to_message_id=update.effective_message.id,
    )
    return ConversationHandler.END