from flask import Flask, render_template, request, url_for
from unicodedata import category

import dao
from TTDHotel.TTDHotel.dao import load_products

app = Flask(__name__)


@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    products = dao.load_products(q=q, cate_id=cate_id)
    return render_template('index.html', products=products)


@app.route('/products/<int:id>')
def details(id):
    product = dao.load_product_by_id(id)
    return render_template('product-details.html', product=product)


@app.route('/home')
def home():
    categories = dao.load_categories()
    return render_template('home.html', categories=categories)


@app.context_processor
def common_attributes():
    return {
        "categories": dao.load_categories()
    }


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)
