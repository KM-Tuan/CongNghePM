import json

from sqlalchemy import cast, func, Integer
from TTDHotel.TTDHotel.utils import hash_password
from TTDHotel.TTDHotel import app, db
from models import Category, Account, RoomStatus, CustomerType, StatusAccount, Role, Employee, Customer, Room, RoomBooked, RoomRented, Bill


# from models import Category
def auth_user(username, password):
    password_hash = hash_password(password)
    return (
        Account.query.options(
            db.joinedload(Account.customer),
            db.joinedload(Account.employee),

        )
        .filter_by(username=username, password=password_hash)
        .first()
    )


def get_or_create_user(user_info):
    """Tạo mới người dùng nếu chưa tồn tại."""
    user = Account.query.filter_by(username=user_info['email']).first()

    if not user:
        user = Account(
            name=user_info['name'],
            username=user_info['email'],
            password=hash_password(user_info['email']),
            avatar=user_info['picture'],
            active=True
        )
        db.session.add(user)
        db.session.commit()

    return user

def add_user(name,phone, username  , password ,address, customer_type_id ,cmnd =None,avatar=None):
    password = hash_password(password)
    tk = Account(username=username, password=password, status=1, role=3)
    db.session.add(tk)
    db.session.commit()

    kh = Customer(name = name, address = address ,phone=phone ,cmnd=cmnd,
                  customer_type_id = customer_type_id, account_id = tk.id,avatar=avatar) #cần giao diện để nhập thông tin
    if avatar:
        kh.avatar = avatar
    db.session.add(kh)
    db.session.commit()


def update_user(id, name=None, phone=None, password=None):
    """Cập nhật thông tin người dùng."""
    customer = Customer.query.filter(Customer.account_id == id).first()
    employee = Employee.query.filter(Employee.account_id == id).first()

    if customer:
        if name:
            customer.name = name
        if phone:
            customer.phone = phone
        db.session.commit()

    if employee:
        if name:
            employee.name = name
        if phone:
            employee.phone = phone
        db.session.commit()

    if password:
        account = Account.query.filter(Account.id == id).first()
        if account:
            account.password = hash_password(password)
            db.session.commit()

    return True


def get_room_status_by_id(room_status_id):
    return RoomStatus.query.get(room_status_id)


def get_all_room_status():
    return RoomStatus.query.all()


def get_customer_type_by_id(customer_type_id):
    return CustomerType.query.get(customer_type_id)


def get_all_customer_types():
    return CustomerType.query.all()


def get_status_account_by_id(status_account_id):
    return StatusAccount.query.get(status_account_id)


def get_all_status_accounts():
    return StatusAccount.query.all()


def get_role_by_id(role_id):
    return Role.query.get(role_id)


def get_all_roles():
    return Role.query.all()


def get_category_by_id(category_id):
    return Category.query.get(category_id)

def get_category_by_name(p):
    return Category.query.filter_by(name=p).first()

def get_all_categories():
    return Category.query.all()


def get_employee_by_id(employee_id):
    return Employee.query.get(employee_id)


def get_all_employees():
    return Employee.query.all()


def get_customer_by_id(customer_id):
    return Customer.query.get(customer_id)


def get_all_customers():
    return Customer.query.all()


def get_room_by_id(room_id):
    return Room.query.get(room_id)


def get_all_rooms():
    return Room.query.all()


def get_room_booked_by_id(room_booked_id):
    return RoomBooked.query.get(room_booked_id)


def get_all_room_booked():
    return RoomBooked.query.all()


def get_room_rented_by_id(room_rented_id):
    return RoomRented.query.get(room_rented_id)


def get_all_room_rented():
    return RoomRented.query.all()


def get_bill_by_id(bill_id):
    return Bill.query.get(bill_id)


def get_all_bills():
    return Bill.query.all()


def get_account_by_id(account_id):
    return Account.query.get(account_id)


def get_account_by_username(username):
    return Account.query.filter_by(username=username).first()


def get_all_accounts():
    return Account.query.all()


# --- Set methods ---
def set_room_status(name):
    room_status = RoomStatus(name=name)
    db.session.add(room_status)
    db.session.commit()

    return room_status


def set_customer_type(name):
    customer_type = CustomerType(name=name)
    db.session.add(customer_type)
    db.session.commit()

    return customer_type


def set_status_account(name):
    status_account = StatusAccount(name=name)

    db.session.add(status_account)
    db.session.commit()

    return status_account


def set_role(name):
    role = Role(name=name)

    db.session.add(role)
    db.session.commit()

    return role


def set_category(name, description, price, image):
    category = Category(name=name, description=description, price=price, image=image)
    db.session.add(category)
    db.session.commit()

    return category


def set_employee(name, cmnd, address, account_id):
    employee = Employee(name=name, cmnd=cmnd, address=address, account_id=account_id)
    db.session.add(employee)
    db.session.commit()

    return employee


def set_customer(name, cmnd, address, phone, customer_type_id, account_id=None):
    customer = Customer(name=name, cmnd=cmnd, address=address, phone=phone, customer_type_id=customer_type_id,
                        account_id=account_id)
    db.session.add(customer)
    db.session.commit()

    return customer


def set_room(status_room, room_type_id):
    room = Room(status_room=status_room, room_type_id=room_type_id)
    db.session.add(room)
    db.session.commit()

    return room


def set_room_booked(customer_id, booking_date, check_in_date, check_out_date):
    room_booked = RoomBooked(customer_id=customer_id, booking_date=booking_date, check_in_date=check_in_date,
                             check_out_date=check_out_date)
    db.session.add(room_booked)
    db.session.commit()

    return room_booked


def set_room_rented(room_booked_id, customer_id, check_in_date, check_out_date, employee_id):
    room_rented = RoomRented(room_booked_id=room_booked_id, customer_id=customer_id, check_in_date=check_in_date,
                             check_out_date=check_out_date, employee_id=employee_id)
    db.session.add(room_rented)
    db.session.commit()

    return room_rented


def set_bill(create_date, charge, total, room_rented_id):
    bill = Bill(create_date=create_date, charge=charge, total=total, room_rented_id=room_rented_id)
    db.session.add(bill)
    db.session.commit()

    return bill


def set_account(username, password, status, role):
    account = Account(username=username, password=password, status=status, role=role)
    db.session.add(account)
    db.session.commit()

    return account

def load_categories():
    # Đọc dữ liệu từ file categories.json
    with open('categories.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        categories = [Category(
            id=category['id'],
            name=category['name'],
            price=category['price'],
            description=category['description'],
            image=category['image']
        ) for category in data]
        return categories


def load_contacts():
    return read_json('data/contacts.json')

def load_rules():
    return read_json('data/rules.json')


def read_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_rules(rules):
    with open('data/rules.json', 'w') as f:
        json.dump(rules, f, indent=4)

def save_contacts(contacts):
    with open('data/contacts.json', 'w') as f:
        json.dump(contacts, f, indent=3)