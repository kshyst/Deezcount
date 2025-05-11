import requests


def get_search_result(search_query):
    url = f"https://snappfood.ir/search/api/v5/search?lat=15.715&long=51.404&query={search_query}"
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

def get_restaurant_list(search_query):
    response = get_search_result(search_query)

    if response:
        restaurants = response['data']['vendor']['items']
        restaurant_list = []
        res_num = 1
        for restaurant in restaurants:
            restaurant_list.append({
                'number': res_num,
                'title': restaurant['title'],
                'code': restaurant['code'],
            })
            res_num += 1
        return restaurant_list
    else:
        print("No data found.")
        return None