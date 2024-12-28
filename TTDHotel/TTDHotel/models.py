from tkinter.font import names

from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.testing.suite.test_reflection import users

from TTDHotel.TTDHotel import app, db

class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    phone = Column(String(11), unique=True, nullable=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(200), default="https://example.com/avatar_default.jpg")
    active = Column(Boolean, default=True)

    def __str__(self):
        return self.name


class Product(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    price = Column(Integer, default=0)
    image = Column(String(300), default="https://example.com/product_default.jpg")

    def __str__(self):
        return self.name


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        import json
        with open('data/products.json', encoding='utf-8') as f:
            products = json.load(f)
            for p in products:
                prod = Product(**p)
                db.session.add(prod)

        db.session.commit()

        import hashlib
        u = User(name="KieuThanhDuc", phone="0987654321", username="admin", password= str(hashlib.md5("123".encode('utf-8')).hexdigest()))
        db.session.add(u)
        db.session.commit()
        pass
