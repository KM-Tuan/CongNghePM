import math

from authlib.integrations.flask_client import OAuth
from flask import render_template, request, redirect, url_for, session, flash
import os
import dao
from TTDHotel.TTDHotel import app, admin


@app.route('/home')
def index():
    logged_in = session.get('logged_in', False)
    q = request.args.get("q")
    cate_id = request.args.get("category_id")
    page = request.args.get("page", 1)
    products = dao.load_products(q=q, cate_id=cate_id, page=page)
    total = dao.count_products()
    if not logged_in:
        session['next'] = request.url
    return render_template('index.html', products=products, logged_in=logged_in, pages = math.ceil(total/app.config['PAGE_SIZE']))


@app.route('/products/<int:id>')
def details(id):
    product = dao.load_product_by_id(id)
    logged_in = session.get('logged_in', False)
    if not logged_in:
        session['next'] = request.url

    return render_template('product-details.html', product=product, logged_in=logged_in)


@app.route('/')
def categories():
    logged_in = session.get('logged_in', False)
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
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(request.referrer)


@app.route('/')
@app.route('/welcome')
def home():
    logged_in = session.get('logged_in', False)
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
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
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
    user = dao.get_or_create_user({
        'id': user_info['id'],
        'email': user_info.get('email'),
        'name': user_info.get('name'),
        'picture': user_info.get('picture')
    })
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


# Cấu hình Facebook OAuth
facebook = oauth.register(
    name='facebook',
    client_id="962541772387140",
    client_secret="1cb70175dd12e7c2ea950b26cd3fe684",
    access_token_url='https://graph.facebook.com/v12.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v12.0/dialog/oauth',
    api_base_url='https://graph.facebook.com/v12.0/',
    client_kwargs={'scope': 'email'}
)


@app.route('/login_facebook')
def login_facebook():
    redirect_uri = url_for('authorize_facebook', _external=True)
    return facebook.authorize_redirect(redirect_uri)


@app.route('/authorize_facebook')
def authorize_facebook():
    token = facebook.authorize_access_token()  # Lấy access token từ Facebook
    resp = facebook.get('me?fields=id,name,email,picture')  # Truy vấn thông tin người dùng
    user_info = resp.json()

    # Xử lý thông tin người dùng
    user = dao.get_or_create_user({
        'id': user_info['id'],
        'email': user_info.get('email'),
        'name': user_info.get('name'),
        'picture': user_info.get('picture', {}).get('data', {}).get('url')
    })

    # Lưu thông tin vào session
    session['profile'] = user_info
    session['logged_in'] = True
    return redirect('/')


@app.route('/logout_facebook')
def logout_facebook():
    session.pop('logged_in', None)
    session.pop('profile', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
