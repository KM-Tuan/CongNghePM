import hashlib
import json
from sqlalchemy import func, cast
from itertools import product

from dns.e164 import query
from sqlalchemy.dialects.postgresql.pg_catalog import quote_ident

from models import *


def load_categories():
    # with open('data/categories.json', encoding='utf-8') as f:
    #     return json.load(f)
    return Category.query.all()

def load_locations():
    # with open('data/categories.json', encoding='utf-8') as f:
    #     return json.load(f)
    return Location.query.all()


def load_products(q=None, cate_id=None, page=None, price=None, location_id=None):
    query = Product.query

    if q:
        query = query.filter(Product.name.contains(q))
    if cate_id:
        query = query.filter(Product.category_id == cate_id)
    if price:
        # Chuyển đổi `price` từ chuỗi sang số để so sánh
        price_column = cast(func.replace(Product.price, ',', ''), Integer)
        if price == '10':  # Dưới 1 triệu
            query = query.filter(price_column < 10000000)
        elif price == '10-20':  # Từ 1 triệu đến 5 triệu
            query = query.filter(price_column.between(10000000, 20000000))
        elif price == '20':  # Trên 5 triệu
            query = query.filter(price_column > 20000000)
    if location_id:
        query = query.filter(Product.location_id == location_id)

    # Phân trang
    if page:
        page_size = app.config['PAGE_SIZE']
        offset = (int(page) - 1) * page_size
        query = query.offset(offset).limit(page_size)

    return query.all()

def count_products(q=None, cate_id=None, price=None, location_id=None):
    query = Product.query

    if q:
        query = query.filter(Product.name.contains(q))
    if cate_id:
        query = query.filter(Product.category_id == cate_id)
    if price:
        # Chuyển đổi `price` từ chuỗi sang số để so sánh
        price_column = cast(func.replace(Product.price, ',', ''), Integer)
        if price == '10':  # Dưới 1 triệu
            query = query.filter(price_column < 10000000)
        elif price == '10-20':  # Từ 1 triệu đến 5 triệu
            query = query.filter(price_column.between(10000000, 20000000))
        elif price == '20':  # Trên 5 triệu
            query = query.filter(price_column > 20000000)
    if location_id:
        query = query.filter(Product.location_id == location_id)

    return query.count()


def auth_user(username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username), User.password.__eq__(password)).first()


def load_product_by_id(id):
    with open('data/products.json', encoding='utf-8') as f:
        products = json.load(f)
        for p in products:
            if p["id"] == id:
                return p

def load_product_by_category_id(id):
    query = Product.query
    if id:
        query = query.filter(Product.category_id.__eq__(id))

    return query.all()


def get_or_create_user(user_info):
    # Kiểm tra xem người dùng đã tồn tại hay chưa
    user = User.query.filter_by(username=user_info['email']).first()

    if not user:
        # Nếu người dùng chưa tồn tại, tạo mới
        user = User(
            name=user_info['name'],
            username=user_info['email'],  # Sử dụng email làm username
            password=hash(user_info['email']),
            avatar=user_info['picture'],
            active=True
        )
        db.session.add(user)
        db.session.commit()

    return user

def add_user(name, phone, username, password, avatar):
    password=hash(password)
    new_user = User(name=name, phone=phone, username=username, password=password, avatar=avatar)
    db.session.add(new_user)
    db.session.commit()

def update_user(id, name, phone):
    user = User.query.get(id)
    if user:
        user.name = name
        user.phone = phone
        db.session.commit()

    return True


def hash(password):
    return str(hashlib.md5(password.encode('utf-8')).hexdigest())