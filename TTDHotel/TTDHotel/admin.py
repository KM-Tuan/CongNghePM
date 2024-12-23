from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Category, Product
from TTDHotel.TTDHotel import app, db

admin = Admin(app, name="TTDHotel", template_mode="bootstrap4")

admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))