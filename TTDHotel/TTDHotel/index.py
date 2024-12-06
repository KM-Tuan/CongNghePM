from flask import Flask, render_template, request, url_for
from unicodedata import category

import dao

app = Flask(__name__)

@app.route('/')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    categories = dao.load_categories()
    products = dao.load_products(q=q, cate_id=cate_id)
    return render_template('index.html', categories=categories, products=products)


@app.route('/products/<int:id>')
def details(id):

    return render_template('product-details.html')

@app.route('/home')
def home():
    categories = dao.load_categories()
    return render_template('home.html', categories=categories)

if __name__ == "__main__":
    app.run(debug=True)