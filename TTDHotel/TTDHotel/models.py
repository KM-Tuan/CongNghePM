from tkinter.font import names

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.testing.suite.test_reflection import users

from TTDHotel.TTDHotel import app, db


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    phone = Column(String(11), unique=True, nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(200), default="https://th.bing.com/th/id/OIP.TD3qZlPaZtEM3dkXOP7f2gHaE7?rs=1&pid=ImgDetMain")
    active = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='category', lazy=True)

    def __str__(self):
        return self.name


class Location(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref='location', lazy=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    address = Column(String(100), nullable=False)
    distance = Column(String(10), nullable=False)
    description = Column(String(100), nullable=False)
    price = Column(String(50), default=0)
    image = Column(String(300), default="https://th.bing.com/th/id/OIP.TD3qZlPaZtEM3dkXOP7f2gHaE7?rs=1&pid=ImgDetMain")
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)
    location_id = Column(Integer, ForeignKey(Location.id), nullable=False)
    rating=Column(Integer, nullable=False)

    def __str__(self):
        return self.name




if __name__ == "__main__":
    with app.app_context():
        # db.create_all()
        # c1 = Category(name="Phòng VIP")
        # c2 = Category(name="Phòng Đôi")
        # c3 = Category(name="Phòng Đơn")
        # l1 = Location(name="TP Hồ Chí Minh")
        # l2 = Location(name="Hà Nội")
        # l3 = Location(name="Vũng Tàu")
        # db.session.add_all([c1, c2, c3, l1, l2, l3])
        # db.session.commit()
        # import json
        # # Lấy category và location bằng cách sử dụng session.get() thay vì query.get()
        # with open('data/products.json', encoding='utf-8') as f:
        #     products = json.load(f)
        #     for p in products:
        #         category = db.session.get(Category, p['category_id'])  # Sử dụng session.get()
        #         location = db.session.get(Location, p['location_id'])  # Sử dụng session.get()
        #         prod = Product(
        #             name=p['name'],
        #             address=p['address'],
        #             distance=p['distance'],
        #             description=p['description'],
        #             price=p['price'],
        #             image=p['image'],
        #             rating=p['rating'],
        #             category=category,  # Sử dụng đối tượng Category thay vì ID
        #             location=location  # Sử dụng đối tượng Location thay vì ID
        #         )
        #         db.session.add(prod)
        #
        # db.session.commit()
        #
        # import hashlib
        # u = User(name="KieuThanhDuc", phone="0987654321", username="admin", password= str(hashlib.md5("123".encode('utf-8')).hexdigest()))
        # db.session.add(u)
        # db.session.commit()
        pass
