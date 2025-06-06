import asyncio

from _base.celery import celery_app
from telegram_bot import get_discounted_products, app
from telegram_user.models import ActiveRestaurant


@celery_app.task(name='tasks.send_discount')
def send_discount(user_id, restaurant_id, restaurant_name):
    print("Sending discount for user {}".format(user_id))
    products = get_discounted_products(restaurant_id)
    if products:
        message = f"محصولات تخفیف خورده در : {restaurant_name} \n"
        for product in products:
            message += str(product)
        asyncio.run(app.bot.send_message(chat_id=user_id, text=message))


@celery_app.task(name="tasks.send_bulk_discounts")
def send_bulk_discounts():
    print("Sending bulk discounts...")

    active_restaurants = ActiveRestaurant.objects.all()
    for restaurant in active_restaurants:
        restaurant_id = restaurant.restaurant.restaurant_code
        restaurant_name = restaurant.restaurant.restaurant_name
        users = restaurant.users.all()

        for user in users:
            if user.does_want_notifications:
                send_discount.delay(user.telegram_id, restaurant_id, restaurant_name)
