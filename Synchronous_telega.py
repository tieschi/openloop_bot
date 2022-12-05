from telebot import TeleBot, types
from configs import Config
from services import DataBaseEdit, normalize_message, get_url
from buttons import get_menu_btn, get_notification_button


bot = TeleBot(Config.TELEGRAM_TOKEN)
db = DataBaseEdit()


@bot.message_handler(commands=['start'])
def cmd_start(message: types.Message):
    bot.send_message(chat_id=message.from_user.id, text='hello!!!', reply_markup=get_menu_btn())


@bot.message_handler(commands=['help'])
def cmd_help(message: types.Message):
    bot.send_message(chat_id=message.from_user.id, text='Add item example:\n'
                     'RopeDemon_Title 34.78\n'
                     'Title_AllThatGlitters 51\n'
                     '<b>/my_items</b> - display a list of all your items\n'
                     '<b>/delete_all</b> - delete_all your items', parse_mode='html'
                     )


@bot.callback_query_handler(func=lambda callback: callback.data)
def update_notification(message: types.CallbackQuery):
    db.update_notification(message.from_user.id, message.data, True)
    bot.send_message(chat_id=message.from_user.id, text=f'notifications enabled for {message.data}')


@bot.message_handler(regexp=r'\S+ (\d+$|\d\.\d+$)')
def save_items(message: types.Message):
    db.save_user_items(normalize_message(message.text), message.from_user.id)
    bot.send_message(chat_id=message.from_user.id, text='items added', reply_markup=get_menu_btn())


@bot.message_handler(commands=['delete_all'])
def cmd_delete_all_items(message: types.Message):
    db.delete_all(message.from_user.id)
    bot.send_message(chat_id=message.from_user.id, text='All items deleted', reply_markup=get_menu_btn())


@bot.message_handler(commands=['my_items'])
def cmd_items_list(message: types.Message):
    items_list = ''
    for item, price in db.get_all_users_items_and_price(message.from_user.id).items():
        items_list += item + ' - ' + str(price) + '\n'
    # bot.send_message(chat_id=message.from_user.id, text=item + ' - ' + str(price))
    m = items_list
    if len(m) > 4095:
        for x in range(0, len(m), 4095):
            bot.send_message(chat_id=message.from_user.id, text=m[x:x + 4095])
    else:
        bot.send_message(chat_id=message.from_user.id, text=str(items_list))


def get_notif(telegram_id, item, price):
    bot.send_message(chat_id=telegram_id,
                     text=item + ' price - ' + str(
                         price) + '\n' + get_url(item),
                     parse_mode='html',
                     reply_markup=get_notification_button(item))


def send_error():
    bot.send_message(chat_id=555248934, text='notifications dropped')


if __name__ == '__main__':
    bot.infinity_polling()
