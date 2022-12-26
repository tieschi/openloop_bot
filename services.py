from sqlalchemy import select, delete, update, insert
from database_connect import Users, ManageDataBase


def normalize_message(text: str):
    dict_items = {}
    list_items = text.split('\n')
    for i in range(len(list_items)):
        list_items[i] = list_items[i].split()
    for item in list_items:
        dict_items[item[0]] = item[1]
    return dict_items


def get_url(item_name):
    url = f'https://openloot.com/items/BT0/{item_name}'
    return url


class DataBaseEdit:
    def __init__(self):
        self.records = ManageDataBase()

    def get_user_items(self, telegram_id):
        record = select(Users.item_name).where(Users.telegram_id == telegram_id)
        return self.records.select_records(record)

    def get_all_users_items_and_price(self, telegram_id):
        record = select(Users.item_name).where(Users.telegram_id == telegram_id)
        items = self.records.select_records(record)
        record = select(Users.item_price).where(Users.telegram_id == telegram_id)
        price = self.records.select_records(record)
        return dict(zip(items, price))

    def save_user_items(self, items: dict, telegram_id: int):
        rows = []
        user_items_list = self.get_user_items(telegram_id)
        for item, price in items.items():
            if item in user_items_list:
                record = update(Users).where(Users.item_name == item).where(Users.telegram_id == telegram_id).values(item_price=price,
                                                                                          notification=True)
                self.records.update_record(record)
            else:
                row = Users(telegram_id=telegram_id,
                            item_name=item,
                            item_price=price,
                            notification=True)
                rows.append(row)

        self.records.insert_records(rows)

    def delete_all(self, telegram_id):
        record = delete(Users).where(Users.telegram_id == telegram_id)
        self.records.delete_records(record)

    def get_all_telegram_id(self):
        record = select(Users.telegram_id).group_by(Users.telegram_id)
        return self.records.select_records(record)

    def get_all_items_from_bd(self):
        record = select(Users.item_name).group_by(Users.item_name)
        return self.records.select_records(record)

    def get_price_from_item(self, item_name, telegram_id):
        record = select(Users.item_price).where(Users.item_name == item_name).filter(Users.telegram_id == telegram_id)
        return self.records.select_records(record)

    def get_telegram_id_from_item_name(self, item_name):
        record = select(Users.telegram_id).where(Users.item_name == item_name)
        return self.records.select_records(record)

    def update_notification(self, telegram_id, item, boole):
        record = update(Users).where(Users.item_name == item).where(Users.telegram_id == telegram_id).values(notification=boole)
        print(record)
        self.records.update_record(record)

    def get_notification_for_item(self, telegram_id, item):
        record = select(Users.notification).where(Users.item_name == item).filter(Users.telegram_id == telegram_id)
        return self.records.select_records(record)[0]

    def get_all_telegram_id_items_price(self):
        record = select(Users.telegram_id, Users.item_name, Users.item_price).order_by(Users.telegram_id)
        return self.records.test_select_records(record)


test = DataBaseEdit()
test.update_notification(317524011, 'GreenGemSeeingEyeRobes_Title', True)
