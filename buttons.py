from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_menu_btn():
    menu_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    btn_my_items = KeyboardButton('/my_items')
    btn_help = KeyboardButton('/help')
    menu_btn.insert(btn_help).insert(btn_my_items)

    return menu_btn


def get_notification_button(item):
    btn = InlineKeyboardMarkup()
    update_notification = InlineKeyboardButton(text='keep watching', callback_data=item)
    btn.insert(update_notification)

    return btn

