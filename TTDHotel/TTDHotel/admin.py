from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Product
from TTDHotel.TTDHotel import app, db

class MyProductView(ModelView):
    column_searchable_list = ['id','name']
    column_filters = ['id','name']

admin = Admin(app, name="TTDHotel", template_mode="bootstrap4")

admin.add_view(MyProductView(Product, db.session))


if __name__ == "__main__":
    app.run(debug=True)