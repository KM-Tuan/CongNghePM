import hashlib
import json
from itertools import product

from sqlalchemy.dialects.postgresql.pg_catalog import quote_ident

from models import *


def load_categories():
    # with open('data/categories.json', encoding='utf-8') as f:
    #     return json.load(f)
    return Category.query.all()


def load_products(q=None, cate_id=None):
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
        query = query.filter(Category.id.__eq__(cate_id))

    return query.all()


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
