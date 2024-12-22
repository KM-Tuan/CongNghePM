import hashlib
import json
from itertools import product

from dns.e164 import query
from sqlalchemy.dialects.postgresql.pg_catalog import quote_ident

from models import *


def load_categories():
    # with open('data/categories.json', encoding='utf-8') as f:
    #     return json.load(f)
    return Category.query.all()


def load_products(q=None, cate_id=None, page=None):
    # with open('data/products.json', encoding='utf-8') as f:
    #     products = json.load(f)
    #     if q:
    #         products = [p for p in products if p["name"].find(q) >= 0]
    #     if cate_id:
    #         products = [p for p in products if p["category_id"].__eq__(int(cate_id))]
    #     return products

    query = Product.query

    if q:
        query = query.filter(Product.name.contains(q))
    if cate_id:
        query = query.filter(Product.category_id.__eq__(cate_id))
        print(f"count: {query.count()}")

    if page:
        page_size = app.config['PAGE_SIZE']
        start = (int(page) - 1) * page_size
        query = query.slice(start, start + page_size)
    return query.all()

def count_products():
    return Product.query.count()

def count_products(cate_id=None):
    query=Product.query
    if cate_id:
        query=query.filter(Product.category_id==cate_id)
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
    gg_id = f"{int(user_info['id']):06}"[:6]
    user = User.query.filter_by(id=gg_id).first()

    if not user:
        # Nếu người dùng chưa tồn tại, tạo mới
        user = User(
            id=gg_id,  # Sử dụng id từ Google
            name=user_info['name'],
            username=user_info['email'],  # Sử dụng email làm username
            password=str(gg_id),  # Chuyển đổi id thành chuỗi cho password (nên mã hóa)
            avatar=user_info['picture'],
            active=True
        )
        db.session.add(user)
        db.session.commit()

    return user