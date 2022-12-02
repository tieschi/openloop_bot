from sqlalchemy import select, delete, update
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

    def get_all_users_items(self, telegram_id):
        record = select(Users.item_name).where(Users.telegram_id == telegram_id)
        return self.records.select_records(record)

    def get_all_users_items_and_price(self, telegram_id):
        record = select(Users.item_name).where(Users.telegram_id == telegram_id)
        items = self.records.select_records(record)
        record = select(Users.item_price).where(Users.telegram_id == telegram_id)
        price = self.records.select_records(record)
        return dict(zip(items, price))

    def save_user_items(self, items: dict, telegram_id):
        for item, price in items.items():
            if item in self.get_all_users_items(telegram_id):
                record = update(Users).where(Users.item_name == item
                                             and Users.telegram_id == telegram_id).values(item_price=price)
                self.records.update_record(record)
            else:
                record = Users(
                    telegram_id=telegram_id,
                    item_name=item,
                    item_price=price,
                    notification=True
                )
                self.records.insert_records([record])

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

    def update_notification_false(self, telegram_id, item):
        record = update(Users).where(Users.item_name == item
                                     and Users.telegram_id == telegram_id).values(notification=False)
        self.records.update_record(record)

    def update_notification_true(self, telegram_id, item):
        record = update(Users).where(Users.item_name == item
                                     and Users.telegram_id == telegram_id).values(notification=True)
        self.records.update_record(record)

    def get_notification_for_item(self, telegram_id, item):
        record = select(Users.notification).where(Users.item_name == item).filter(Users.telegram_id == telegram_id)
        return self.records.select_records(record)[0]


# db = DataBaseEdit()
# print(db.get_price_from_item('FixerSingleEye_Chest', 555248934))
# print(db.get_price_from_item('FixerSingleEye_Chest', 431796930))
# print(db.get_price_from_item('CrystalBlue_Title')[0])
