import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker
import json
from models import create_tables, Publisher, Shop, Book, Stock, Sale
from pprint import pprint

DNS = "postgresql://postgres:77601300@localhost:5432/booksales"
engine = sq.create_engine(DNS)

create_tables(engine)


Session = sessionmaker(bind=engine)
session = Session()


with open('tests_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
# pprint(data)


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
    sale = Sale(price=item["fields"]["price"], date_sale=item["fields"]["date_sale"], id_stock=item["fields"]["stock"], count=item["fields"]["count"])
    session.add(sale)


session.commit()

session.close()


Session = sessionmaker(bind=engine)
session = Session()


# Ввод издателя (publisher)
publisher_name = input("Введите имя издателя: ")

# Запрос выборки магазинов, продающих целевого издателя
shops = session.query(Shop).join(Stock).join(Book).join(Publisher).filter(Publisher.name == publisher_name).all()

# Вывод результатов
if shops:
    print(f"Магазины, продающие издателя {publisher_name}:")
    for shop in shops:
        print(shop.name)
else:
    print(f"Магазины, продающие издателя {publisher_name}, не найдены")


session.commit()

session.close()