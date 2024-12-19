from flask import render_template, request, redirect, session, url_for

import dao
from TTDHotel.TTDHotel import app


@app.route('/home')
def index():
    logged_in = session.get('logged_in',False)
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    products = dao.load_products(q=q, cate_id=cate_id)
    session['next'] = request.url
    return render_template('index.html', products=products, logged_in=logged_in)


@app.route('/products/<int:id>')
def details(id):
    product = dao.load_product_by_id(id)
    logged_in = session.get('logged_in',False)
    if not logged_in:
        session['next'] = request.url

    return render_template('product-details.html', product=product, logged_in=logged_in)

@app.route('/')
def categories():
    logged_in = session.get('logged_in',False)
    category_id = request.args.get('category_id')
    products = dao.load_product_by_category_id(category_id)
    return render_template('index.html', products=products, logged_in=logged_in)



@app.route('/login', methods=['get', 'post'])
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username, password)
        if user:
            session['logged_in'] = True
            next_page = session.get('next')
            return redirect(next_page)

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    return redirect(request.referrer)


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
