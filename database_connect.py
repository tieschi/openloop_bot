from sqlalchemy.orm import Session
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy import create_engine
from configs import Config
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Boolean
from itertools import chain

Base = declarative_base()


class ManageDataBase:
    ENGINE = None

    def __init__(self):
        url = f'postgresql://{Config.DB_USER}:{Config.DB_PASS}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}'
        if not database_exists(url):
            create_database(url)
        ManageDataBase.ENGINE = create_engine(url, echo=False, pool_size=30, max_overflow=15) if not  \
            ManageDataBase.ENGINE else ManageDataBase.ENGINE

        self.engine = ManageDataBase.ENGINE

    def create_db(self):
        Base.metadata.create_all(self.engine)

    def insert_records(self, records):
        session = Session(self.engine)
        for record in records:
            session.add(record)
            session.commit()

    def select_records(self, records):
        session = Session(self.engine)
        result = session.execute(records).all()
        session.close()
        return list(chain(*result))

    def delete_records(self, records):
        session = Session(self.engine)
        session.execute(records)
        session.commit()

    def update_record(self, record):
        with Session(self.engine) as session:
            session.execute(record)
            session.commit()


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer)
    item_name = Column(String)
    item_price = Column(Float)
    notification = Column(Boolean)


if __name__ == '__main__':
    ManageDataBase().create_db()
