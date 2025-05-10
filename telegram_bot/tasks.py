import asyncio

from celery import Celery, shared_task

from telegram_bot import get_discounted_products, app

celery_app = Celery('deezcount', broker='redis://localhost:6379/0')

@celery_app.task(name='tasks.send_discount')
def send_discount(user_id, restaurant_id):

    print("Sending discount for user {}".format(user_id))
    products = get_discounted_products(restaurant_id)
    if products:
        message = f"Discounted products in restaurant {restaurant_id}:\n"
        for product in products:
            message += str(product)
        asyncio.run(app.bot.send_message(chat_id=user_id, text=message))
    else:
        asyncio.run(app.bot.send_message(chat_id=user_id, text="No discounted products found."))


celery_app.conf.beat_schedule = {
    'send-discounts-every-15-min': {
        'task': 'tasks.send_bulk_discounts',
        'schedule': 10,
    },
}


@celery_app.task( name="tasks.send_bulk_discounts")
def send_bulk_discounts():
    print("Sending bulk discounts...")
    users = ['91003546']
    for user in users:
        send_discount.delay(user, "0m1wvz")
