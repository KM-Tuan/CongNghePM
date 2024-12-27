import math

from authlib.integrations.flask_client import OAuth
from django.contrib.messages import success
from flask import render_template, request, redirect, url_for, session, flash
import os
import dao
from TTDHotel.TTDHotel import app, oauth, facebook, admin
import  cloudinary.uploader
@app.route('/home')
def index():
    logged_in = session.get('logged_in', False)
    q = request.args.get("q")
    cate_id = request.args.get("category_id", '').strip()
    location_id = request.args.get('location', '').strip()
    price=request.args.get('price','').strip()
    page = request.args.get("page",1)

    categories=dao.load_categories()
    locations=dao.load_locations()

    total = dao.count_products(q=q, cate_id=cate_id, price=price, location_id=location_id)
    products = dao.load_products(q=q, cate_id=cate_id, page=page, price=price, location_id=location_id)
    if not logged_in:
        session['next'] = request.url
    return render_template('index.html',locations=locations,categories=categories, products=products, logged_in=logged_in, pages = math.ceil(total/app.config['PAGE_SIZE']))


@app.template_filter('dict_without_key')
def dict_without_key(d, key):
    return {k: v for k, v in d.items() if k != key}


@app.route('/products/<int:id>')
def details(id):
    product = dao.load_product_by_id(id)
    logged_in = session.get('logged_in', False)
    if not logged_in:
        session['next'] = request.url

    return render_template('product-details.html', product=product, logged_in=logged_in)


@app.route('/categories')
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
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['logged_in'] = True
            session['phone'] = user.phone
            next_page = session.get('next')
            return redirect(next_page)
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')


@app.context_processor
def get_user():
    user_id=session.get('user_id')
    user_name=session.get('user_name')
    phone=session.get('phone')
    logged_in=session.get('logged_in')
    return dict(user_id=user_id, user_name=user_name, phone=phone, logged_in=logged_in)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    for key in list(session.keys()):
        session.pop(key)
    return redirect(request.referrer)


@app.route('/info', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        id = session.get('user_id')
        name = request.form.get('name')
        phone = request.form.get('phone')

        if len(phone) < 10 or not phone.isdigit():
            flash('Số điện thoại không hợp lệ. Vui lòng nhập số điện thoại gồm ít nhất 10 chữ số.', 'danger')
            return redirect(request.referrer)

        if not name or not phone:
            flash('Tên và số điện thoại không được để trống.', 'danger')
            return redirect(request.referrer)

        success = dao.update_user(id, name=name, phone=phone)
        if success:
            session['user_name'] = name
            session['phone'] = phone
            flash('Cập nhật thông tin thành công.', 'success')
        else:
            pass
            flash('Đã xảy ra lỗi khi cập nhật thông tin. Vui lòng thử lại.', 'danger')

        return redirect(request.referrer)

@app.route('/changePassword', methods=['GET', 'POST'])
def update_password():
    global success
    if request.method == 'POST':
        id = session.get('user_id')
        oldPassword = request.form.get('oldPassword')
        newPassword = request.form.get('newPassword')
        confirm = request.form.get('confirm')


        if newPassword != confirm:
            flash('Không trùng khớp.', 'danger')
            redirect(request.referrer)

        user= dao.get_user_by_id(id)
        if user:
            if user.password == dao.hash(oldPassword):
                success = dao.update_user(id,  password=newPassword)
            else:
                flash('Mật khẩu không hợp lệ. Vui lòng thử lại.', 'danger')
                success=False

            if success:
                flash('Cập nhật thông tin thành công.', 'success')
            else:
                flash('Đã xảy ra lỗi khi cập nhật thông tin. Vui lòng thử lại.', 'danger')


        return redirect(request.referrer)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':  # Phương thức POST
        name = request.form.get('name')
        phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        avatar = request.files.get('avatar')  # Lấy tệp ảnh tải lên
        avatar_path=None

        # Kiểm tra xác nhận mật khẩu
        if password != confirm:
            flash('Passwords do not match. Please try again.', 'danger')
            return render_template('register.html')

        # Kiểm tra xem tài khoản đã tồn tại chưa
        user = dao.auth_user(username,password)  # Hàm kiểm tra người dùng, bạn cần định nghĩa
        if user:
            flash('Username already exists. Please try a different username.', 'danger')
            return render_template('register.html')

        # Lưu hình ảnh vào thư mục 'static/images'
        if avatar:
            filename = avatar.filename
            if avatar:
                res =cloudinary.uploader.upload(avatar)
                avatar_path = res['secure_url']
            # avatar.save(os.path.join('static/images/', filename))  # Lưu tệp

        # Thêm người dùng vào cơ sở dữ liệu
        dao.add_user(name=name, phone=phone, username=username, password=password, avatar=avatar.filename)

        flash('Account created successfully!', 'success')
        return redirect('/login')  # Điều hướng đến trang đăng nhập

    return render_template('register.html')  # Hiển thị form đăng ký

@app.route('/')
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
        'email': user_info.get('email'),
        'name': user_info.get('name'),
        'picture': user_info.get('picture')
    })
    # and set ur own data in the session not the profile from Google
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    session['logged_in'] = True
    session['user_name'] = user.name
    next_page = session.get('next')
    return redirect(next_page)


@app.route('/logout_google')
def logout_google():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')





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
        'email': user_info.get('email'),
        'name': user_info.get('name'),
        'picture': user_info.get('picture', {}).get('data', {}).get('url')
    })

    # Lưu thông tin vào session
    session['profile'] = user_info
    session['logged_in'] = True
    session['user_name'] = user.name
    next_page = session.get('next')
    return redirect(next_page)


@app.route('/logout_facebook')
def logout_facebook():
    session.pop('logged_in', None)
    session.pop('profile', None)
    return redirect('/')


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
