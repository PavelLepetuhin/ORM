import json

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from config import login, password
from models import create_tables, Publisher, Shop, Book, Stock, Sale


DNS = f"postgresql://{login}:{password}@localhost:5432/booksales"
engine = sq.create_engine(DNS)

create_tables(engine)


def input_value():
    user_input = input("Введите значение: ")
    try:
        value = int(user_input)
    except ValueError:
        value = user_input
    return value


Session = sessionmaker(bind=engine)
session = Session()

with open('tests_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


pub = (item for item in data if item["model"] == "publisher")
for item in pub:
    publisher = Publisher(name=item["fields"]["name"])
    session.add(publisher)

shop = (item for item in data if item["model"] == "shop")
for item in shop:
    shop = Shop(name=item["fields"]["name"])
    session.add(shop)

book = (item for item in data if item["model"] == "book")
for item in book:
    book = Book(title=item["fields"]["title"], id_publisher=item["fields"]["publisher"])
    session.add(book)

stock = (item for item in data if item["model"] == "stock")
for item in stock:
    stock = Stock(id_book=item["fields"]["book"], count=item["fields"]["count"], id_shop=item["fields"]["shop"])
    session.add(stock)

sale = (item for item in data if item["model"] == "sale")
for item in sale:
    sale = Sale(price=item["fields"]["price"], date_sale=item["fields"]["date_sale"], id_stock=item["fields"]["stock"],
                count=item["fields"]["count"])
    session.add(sale)

session.commit()
session.close()

Session = sessionmaker(bind=engine)
session = Session()


# Ввод издателя (publisher)
publisher_name = input_value()

if type(publisher_name) == str:
    shops = session.query(Stock).join(Book).join(Publisher).join(Shop).join(Sale).filter(
        Publisher.name == publisher_name).all()
    print(f"Продажа книг издателя {publisher_name}:")
    for shop in shops:
        date_ = session.query(Sale).filter(Sale.id_stock == shop.id).first().date_sale
        price_ = session.query(Sale).filter(Sale.id_stock == shop.id).first().price
        print(f'{shop.book.title} | {shop.shop.name} | {date_} | {price_}')
elif type(publisher_name) == int:
    try:
        shops = session.query(Stock).join(Book).join(Publisher).join(Shop).join(Sale).filter(
            Publisher.id == publisher_name).all()
        publisher_name = session.query(Publisher).filter(Publisher.id == publisher_name).first().name
        print(f"Продажа книг издателя {publisher_name}:")
        for shop in shops:
            date_ = session.query(Sale).filter(Sale.id_stock == shop.id).first().date_sale
            price_ = session.query(Sale).filter(Sale.id_stock == shop.id).first().price
            print(f'{shop.book.title} | {shop.shop.name} | {date_} | {price_}')
    except AttributeError:
        print("Такого издателя нет в базе данных")
        exit()


session.commit()
session.close()
