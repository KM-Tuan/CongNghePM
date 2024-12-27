from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from models import Category, Product, Location
from TTDHotel.TTDHotel import app, db

class MyCategoryView(ModelView):
    column_list = ['name', 'products']
    column_searchable_list = ['id','name']

class MyProductView(ModelView):
    column_searchable_list = ['id','name']
    column_filters = ['id','name']

class MyLocationView(ModelView):
    column_searchable_list = ['id','name']
    column_filters = ['id','name']


admin = Admin(app, name="TTDHotel", template_mode="bootstrap4")

admin.add_view(MyCategoryView(Category, db.session))
admin.add_view(MyProductView(Product, db.session))
admin.add_view(MyLocationView(Location, db.session))


if __name__ == "__main__":
    app.run(debug=True)