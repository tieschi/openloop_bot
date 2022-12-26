import time
import requests
from services import DataBaseEdit, get_url
import sqlalchemy.exc
from telebot import TeleBot
from configs import Config
from buttons import get_notification_button


bot = TeleBot(Config.TELEGRAM_TOKEN)
db = DataBaseEdit()


def get_notif(telegram_id, item, price):
    bot.send_message(chat_id=telegram_id,
                     text=item + ' price - ' + str(
                         price) + '\n' + get_url(item),
                     parse_mode='html',
                     reply_markup=get_notification_button(item))


def send_error():
    bot.send_message(chat_id=555248934, text='notifications dropped')


def get_all_items():
    items_dict = {}
    for i in range(1, 4):
        url = f'https://openloot.com/api/market/' \
              f'options?gameId=56a149cf-f146-487a-8a1c-58dc9ff3a15c&' \
              f'order=name&page={i}&pageSize=100&primary=false&sort=asc'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0,gzip(gfe)'
        }
        try:
            response = requests.get(url=url, headers=headers).json()
            time.sleep(5)
        except requests.exceptions.JSONDecodeError:
            print(f'Нет доступа к странице {i}')
            time.sleep(5)
            continue
        for num_item in range(len(response['items'])):
            item_name = response['items'][num_item]['optionName']
            item_price = response['items'][num_item]['lowestPrice']
            items_dict[item_name] = item_price

    return items_dict


def new_notifications():
    while True:
        items = get_all_items()
        for info_list in db.get_all_telegram_id_items_price():
            telegram_id = info_list[0]
            item_name = info_list[1]
            item_price = info_list[2]
            print(db.get_all_telegram_id_items_price())
            try:
                if item_name in items:
                    notif = db.get_notification_for_item(telegram_id, item_name)
                    if item_name == 'GreenGemSeeingEyeRobes_Title':
                        print(telegram_id, notif)
                    if item_price >= items[item_name] and notif:
                        db.update_notification(telegram_id, item_name, False)
                        get_notif(telegram_id, item_name, items[item_name])
                    elif item_price < items[item_name] and not notif:
                        db.update_notification(telegram_id, item_name, True)
            except sqlalchemy.exc.TimeoutError:
                send_error()
                continue


# def get_all_items_test():
#     items_dict = {}
#     # for i in range(1, 4):
#         # await asyncio.sleep(5)
#     url = f'https://openloot.com/api/market/' \
#           f'options?gameId=56a149cf-f146-487a-8a1c-58dc9ff3a15c&' \
#           f'order=name&page=3&pageSize=100&primary=false&sort=asc'
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0,gzip(gfe)'
#     }
#     # try:
#     response = requests.get(url=url, headers=headers).json()
#     # except requests.exceptions.JSONDecodeError:
#         # print('Нет доступа к странице ---------------------------------------')
#         # continue
#     for num_item in range(len(response['items'])):
#         print(response['items'][num_item]['optionName'], 1000)


# get_all_items_test()


if __name__ == '__main__':
    new_notifications()
