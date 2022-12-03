import asyncio
import requests
from aiogram import Dispatcher, Bot, types, executor
from configs import Config
from services import DataBaseEdit, normalize_message, get_url
from buttons import get_menu_btn, get_notification_button

token = Config.TELEGRAM_TOKEN
bot = Bot(token)
dp = Dispatcher(bot)
db = DataBaseEdit()


async def on_startup(_):
    print('bot is running')


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await message.answer(text='hello!!!', reply_markup=get_menu_btn())


@dp.message_handler(commands=['help'])
async def cmd_help(message: types.Message):
    await message.answer(text='Add item example:\n'
                              'RopeDemon_Title 34.78\n'
                              'Title_AllThatGlitters 51\n'
                              '<b>/my_items</b> - display a list of all your items\n'
                              '<b>/delete_all</b> - delete_all your items', parse_mode='html'
                         )


@dp.callback_query_handler()
async def update_notification(message: types.CallbackQuery):
    db.update_notification_true(message.from_user.id, message.data)
    await message.answer(text=f'notifications enabled for {message.data}')


@dp.message_handler(regexp=r'\S+ \d+|\d\.\d+$')
async def save_items(message: types.Message):
    await message.answer(text='items added', reply_markup=get_menu_btn())
    db.save_user_items(normalize_message(message.text), message.from_user.id)


@dp.message_handler(commands=['delete_all'])
async def cmd_delete_all_items(message: types.Message):
    db.delete_all(message.from_user.id)
    await message.answer(text='All items deleted', reply_markup=get_menu_btn())


@dp.message_handler(commands=['my_items'])
async def cmd_items_list(message: types.Message):
    for item, price in db.get_all_users_items_and_price(message.from_user.id).items():
        await message.answer(text=item + ' - ' + str(price))


async def get_notifications():
    while True:
        items_dict = {}
        for i in range(1, 4):
            await asyncio.sleep(5)
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

        for telegram_id in db.get_all_telegram_id():
            for item in db.get_user_items(telegram_id):
                if item in items_dict:
                    if db.get_price_from_item(item, telegram_id)[0] > items_dict[item]:
                        if db.get_notification_for_item(telegram_id, item):
                            db.update_notification_false(telegram_id, item)
                            await bot.send_message(chat_id=telegram_id,
                                                   text=item + ' price - ' + str(
                                                       items_dict[item]) + '\n' + get_url(item),
                                                   parse_mode='html',
                                                   reply_markup=get_notification_button(item))


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(get_notifications())
    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup
    )
    loop.run_forever()
