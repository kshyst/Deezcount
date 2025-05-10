import requests

from models.product import Product


def get_restaurant_menu(restaurant_id):
    url = f"https://apigw.snappfood.ir/menu-read-model/{restaurant_id}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_menu_items(menu:dict):
    discounted_items = []
    for cat in menu['data']['menuCategories']:
        for product in cat['products']:
            if product['variations'][0]['discount']:
                discounted_items.append(product)

    return discounted_items


def get_discounted_products(restaurant_id):
    discounted_products = get_menu_items(get_restaurant_menu(restaurant_id))

    products = []

    for discounted_product in discounted_products:
        p = Product(discounted_product['title'], discounted_product['variations'][0]['price'], discounted_product['variations'][0]['discount']['amount'])
        products.append(p)

    return products