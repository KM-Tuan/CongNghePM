import math
from datetime import datetime

from authlib.integrations.flask_client import OAuth
from django.contrib.messages import success
from flask import render_template, request, redirect, url_for, session, flash
import os
import unicodedata
from flask_login import login_user, logout_user, current_user, login_required

import dao
from TTDHotel.TTDHotel import app, oauth, facebook, admin, login, db
import  cloudinary.uploader

from TTDHotel.TTDHotel.dao import set_room_booked
from models import Customer


def check_login():
    logged_in = session.get('logged_in', False)
    if not logged_in:
        session['next'] = request.url
    return logged_in

@app.route('/home')
def index():
    return render_template('welcome.html', logged_in=check_login())

@app.template_filter('dict_without_key')
def dict_without_key(d, key):
    return {k: v for k, v in d.items() if k != key}

@app.route('/booking',methods=['GET','POST'])
def show_categories():
    categories = dao.get_all_categories()
    list_category = dao.get_all_categories()
    if request.method == "POST":
        name = request.form.get('name')
        phone = request.form.get('phone')
        cmnd = request.form.get('cmnd')
        customer_type_id = request.form.get('option')
        customer= Customer(name=name, phone=phone, cmnd=cmnd, type_id=customer_type_id)
        db.session.add(customer)
        db.session.commit()
        pass

    return render_template('index.html', categories=categories, list_category=list_category, logged_in=check_login())


@app.route('/filter_category', methods=['POST'])
def filter_category():
    selected_value = request.form.get('loai_phong')  # Get selected category ID
    list_category = dao.get_all_categories()
    category = dao.get_all_categories()
    if selected_value:
        categories = dao.get_category_by_id(selected_value)
        categories = [categories] if categories else []
    else:
        categories = dao.get_all_categories()

    return render_template('index.html', list_category=list_category,categories=categories, category=category, selected_value=selected_value,
                           logged_in=check_login())


@app.route('/rules')
def rules():
    rules = dao.load_rules()
    return render_template('rules.html', logged_in=check_login(), rules=rules)

@app.route('/contacts')
def contacts():
    contacts = dao.load_contacts()
    return render_template('contacts.html', logged_in=check_login(), contacts=contacts)


@app.route('/category/<int:id>')
def details(id):
    category = dao.get_category_by_id(id)
    return render_template('product-details.html', category=category, logged_in=check_login())

@app.route('/booked', methods=['POST'])
def booked():
    role = session.get('user_role')
    if role == 3:
        customer_id=session.get('user_id')
        customer_name = request.form['name']
        customer_phone=request.form['phone']
        customer_id_card=request.form['cmnd']
        customer_type=request.form['option']
        check_in_date=datetime.strptime(request.form['check_in_date'],'%Y-%m-%d')
        check_out_date=datetime.strptime(request.form['check_out_date'],'%Y-%m-%d')

        room_booked = set_room_booked(customer_id=customer_id,booking_date=datetime.now(),check_in_date=check_in_date,check_out_date=check_out_date)
        db.session.add(room_booked)
        db.session.flush()

        # booking_details=set_booking_details(room_booked_id=room_booked.id, room_id=room)

@app.route('/history')
def history():
    bookings = dao.get_all_room_booked()
    return render_template('history.html', bookings=bookings, logged_in=check_login())


@app.route('/admin-login', methods=['GET', 'POST'])
def process_admin_login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username, password)
        if user:
            set_user_session(user)
            login_user(user)
        return redirect('/admin')


@login.user_loader
def get_user_by_id(user_id):
    return dao.get_user_by_id(int(user_id))


@app.route('/login', methods=['GET', 'POST'])
def login_my_user():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username, password)
        if user:
            set_user_session(user)
            login_user(user)
            next_page = session.get('next', '/')
            return redirect(next_page)
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

def set_user_session(user):
    session['user_id'] = user.id
    session['user_role']=user.role
    session['user_name'] = (
        user.customer.name if user.customer else
        user.employee.name if user.employee else
        "Admin"
    )
    session['logged_in'] = True
    session['phone'] = user.customer.phone if user.customer else user.employee.phone if user.employee else "None"





@app.context_processor
def get_user():
    user_id = session.get('user_id')
    user_name = session.get('user_name')
    phone = session.get('phone')
    role = session.get('user_role')
    logged_in = session.get('logged_in')
    return dict(user_id=user_id, user_name=user_name, phone=phone, role=role, logged_in=logged_in)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(request.referrer or '/')

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
            flash('Đã xảy ra lỗi khi cập nhật thông tin. Vui lòng thử lại.', 'danger')

    return redirect(request.referrer)

@app.route('/changePassword', methods=['GET', 'POST'])
def update_password():
    if request.method == 'POST':
        id = session.get('user_id')
        old_password = request.form.get('oldPassword')
        new_password = request.form.get('newPassword')
        confirm = request.form.get('confirm')

        if new_password != confirm:
            flash('Không trùng khớp.', 'danger')
            return redirect(request.referrer)

        user = dao.get_user_by_id(id)
        if user:
            if user.password == dao.hash(old_password):
                success = dao.update_user(id, password=new_password)
                if success:
                    flash('Cập nhật mật khẩu thành công.', 'success')
                else:
                    flash('Đã xảy ra lỗi khi cập nhật mật khẩu. Vui lòng thử lại.', 'danger')
            else:
                flash('Mật khẩu hiện tại không đúng.', 'danger')
        return redirect(request.referrer)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get('password')
        confirm = request.form.get('confirm')
        avatar = request.files.get('avatar')
        address = request.form.get('address')
        cmnd= request.form.get('cmnd')
        customer_type = request.form.get('customer_type')
        avatar_path = None
        role = request.form.get('role')  # Nhận role từ form

        if password != confirm:
            flash('Passwords do not match. Please try again.', 'danger')
            return render_template('register.html')

        if dao.auth_user(username, password):
            flash('Username already exists. Please try a different username.', 'danger')
            return render_template('register.html')

        if avatar:
            res = cloudinary.uploader.upload(avatar)
            avatar_path = res['secure_url']

        success = dao.add_user(name=name, phone=phone, username=username, password=password,
                               customer_type_id=customer_type, address=address, cmnd=cmnd,  avatar=avatar_path)
        if success:
            flash('Account created successfully!', 'success')
            return redirect('/login')
        else:
            flash('An error occurred while creating the account. Please try again.', 'danger')

    return render_template('register.html')


@app.route('/')
def home():
    logged_in = session.get('logged_in', False)
    if not logged_in:
        session['next'] = request.url
    return render_template('welcome.html', logged_in=logged_in)


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
    session['user_name'] = user_info['name']
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
    session['user_name'] = user_info['name']
    next_page = session.get('next')
    return redirect(next_page)


@app.route('/logout_facebook')
def logout_facebook():
    session.pop('logged_in', None)
    session.pop('profile', None)
    return redirect('/')


@app.route('/routes')
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        url = urllib.parse.unquote(f"{rule}")
        output.append(f"{rule.endpoint}: {url} [{methods}]")
    return "<br>".join(output)

if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
