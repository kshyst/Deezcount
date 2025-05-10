import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36'
}
restaurant_menu = requests.get("https://apigw.snappfood.ir/menu-read-model/0m1wvz", headers=headers)

print(type(restaurant_menu.json()))

def get_menu_items(menu:dict):
    discounted_items = []
    for cat in menu['data']['menuCategories']:
        for product in cat['products']:
            if product['variations'][0]['discount']:
                discounted_items.append(product)


    return discounted_items

discounted_products = get_menu_items(restaurant_menu.json())

for product in discounted_products:
    print(product['title'])
    print(f"Discount: {product['variations'][0]['discount']['amount']}")
    print(f"Price: {product['variations'][0]['price']}")
    print("-" * 20)