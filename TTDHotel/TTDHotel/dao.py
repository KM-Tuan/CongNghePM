import hashlib
import json

from sqlalchemy import cast, func, Integer

from TTDHotel.TTDHotel import app
# from models import Category

def hash_password(password):
    """Mã hóa mật khẩu bằng cách sử dụng MD5."""
    return hashlib.md5(password.encode('utf-8')).hexdigest()


def load_categories(q=None):
    """Tải các sản phẩm từ cơ sở dữ liệu với các bộ lọc."""
    query = Category.query

    if q:
        query = query.filter(Category.name.contains(q))

    return query.all()

def count_products(q=None):
    """Đếm số lượng sản phẩm với các bộ lọc."""
    query = Product.query

    if q:
        query = query.filter(Product.name.contains(q))

    return query.count()

def auth_user(username, password):
    """Xác thực người dùng với mật khẩu đã mã hóa."""
    password_hash = hash_password(password)
    return Account.query.filter_by(username=username, password=password_hash).first()

def load_product_by_id(id):
    """Tải sản phẩm theo ID từ cơ sở dữ liệu."""
    return Product.query.get(id)

def get_or_create_user(user_info):
    """Tạo mới người dùng nếu chưa tồn tại."""
    user = User.query.filter_by(username=user_info['email']).first()

    if not user:
        user = User(
            name=user_info['name'],
            username=user_info['email'],
            password=hash_password(user_info['email']),
            avatar=user_info['picture'],
            active=True
        )
        db.session.add(user)
        db.session.commit()

    return user

def add_user(name, phone, username, password, avatar):
    """Thêm người dùng mới."""
    password_hash = hash_password(password)
    new_user = User(name=name, phone=phone, username=username, password=password_hash, avatar=avatar)
    db.session.add(new_user)
    db.session.commit()

def get_user_by_id(id):
    """Lấy người dùng theo ID."""
    return User.query.get(id)

def update_user(id, name=None, phone=None, password=None):
    """Cập nhật thông tin người dùng."""
    user = User.query.get(id)
    if user:
        if name:
            user.name = name
        if phone:
            user.phone = phone
        if password:
            user.password = hash_password(password)
        db.session.commit()
    else:
        return False

    return True

def load_rules():
    return read_json('data/rules.json')

def read_json(path):
    with open(path, 'r') as f:
        return json.load(f)

def save_rules(rules):
    with open('data/rules.json', 'w') as f:
        json.dump(rules, f, indent=4)