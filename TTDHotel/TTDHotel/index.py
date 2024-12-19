from flask import render_template, request, redirect

import dao
from TTDHotel.TTDHotel import app


@app.route('/home')
def index():
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    products = dao.load_products(q=q, cate_id=cate_id)
    return render_template('index.html', products=products)


@app.route('/products/<int:id>')
def details(id):
    product = dao.load_product_by_id(id)
    return render_template('product-details.html', product=product)

@app.route('/')
def categories():
    category_id = request.args.get('category_id')
    products = dao.load_product_by_category_id(category_id)
    return render_template('index.html', products=products)



@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username, password)
        if user:
            return redirect('/')

    return render_template('login.html')


@app.route('/')
@app.route('/welcome')
def home():
    categories = dao.load_categories()
    return render_template('welcome.html', categories=categories)


@app.context_processor
def common_attributes():
    return {
        "categories": dao.load_categories()
    }


if __name__ == "__main__":
    app.run(debug=True)
