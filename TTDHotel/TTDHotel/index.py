from authlib.integrations.flask_client import OAuth
from flask import render_template, request, redirect,url_for, session, flash
from dotenv import load_dotenv
import os

from pyexpat.errors import messages

import dao
from TTDHotel.TTDHotel import app


@app.route('/home')
def index():
    logged_in = session.get('logged_in',False)
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    products = dao.load_products(q=q, cate_id=cate_id)
    if not logged_in:
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
    if not logged_in:
        session['next'] = request.url
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
    flash('Cút', 'success')
    return redirect(request.referrer)


@app.route('/')
@app.route('/welcome')
def home():
    logged_in = session.get('logged_in',False)
    categories = dao.load_categories()
    if not logged_in:
        session['next'] = request.url
    return render_template('welcome.html', categories=categories, logged_in=logged_in)


@app.context_processor
def common_attributes():
    return {
        "categories": dao.load_categories()
    }

###################

# Truy xuất giá trị môi trường
google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_client_secret = os.getenv('GOOGLE_CLIENT_SECRET')

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="294714413960-kceqf54eu6rrkh9af98pj9n5ehtmpf8q.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)


@app.route('/login_google')
def login_google():
    google = oauth.create_client('google')  # create the Google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the Google oauth client
    token = google.authorize_access_token()  # Access token from Google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
    # Here you use the profile/user data that you got and query your database find/register the user
    user = dao.get_or_create_user(user_info)
    # and set ur own data in the session not the profile from Google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    session['logged_in'] = True
    return redirect('/')


@app.route('/logout_google')
def logout_google():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')



if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
