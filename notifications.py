import requests
from Synchronous_telega import *
from services import DataBaseEdit
import time
import sqlalchemy.exc

db = DataBaseEdit()


def get_all_items():
    items_dict = {}
    for i in range(1, 4):
        # await asyncio.sleep(5)
        url = f'https://openloot.com/api/market/' \
              f'options?gameId=56a149cf-f146-487a-8a1c-58dc9ff3a15c&' \
              f'order=name&page={i}&pageSize=100&primary=false&sort=asc'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0,gzip(gfe)'
        }
        try:
            response = requests.get(url=url, headers=headers).json()
        except requests.exceptions.JSONDecodeError:
            # print('Нет доступа к странице -')
            continue
        for num_item in range(len(response['items'])):
            item_name = response['items'][num_item]['optionName']
            item_price = response['items'][num_item]['lowestPrice']
            items_dict[item_name] = item_price

    return items_dict


def notifications():
    items = get_all_items()
    for telegram_id in db.get_all_telegram_id():
        for item in db.get_user_items(telegram_id):
            try:
                if item in items:
                    if db.get_price_from_item(item, telegram_id)[0] >= items[item]:
                        if db.get_notification_for_item(telegram_id, item):
                            db.update_notification(telegram_id, item, False)
                            get_notif(telegram_id, item, items[item])
            except sqlalchemy.exc.TimeoutError:
                print('error')
                send_error()
                continue


# def get_all_items_test():
#     items_dict = {}
#     for i in range(1, 4):
#         # await asyncio.sleep(5)
#         url = f'https://openloot.com/api/market/' \
#               f'options?gameId=56a149cf-f146-487a-8a1c-58dc9ff3a15c&' \
#               f'order=name&page={i}&pageSize=100&primary=false&sort=asc'
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0,gzip(gfe)'
#         }
#         try:
#             response = requests.get(url=url, headers=headers).json()
#         except requests.exceptions.JSONDecodeError:
#             print('Нет доступа к странице ---------------------------------------')
#             continue
#         for num_item in range(len(response['items'])):
#             print(response['items'][num_item]['optionName'], 0.1)


while True:
    notifications()
    time.sleep(5)
