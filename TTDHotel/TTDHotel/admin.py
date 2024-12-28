from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from TTDHotel.TTDHotel import app, db
from models import Category


class MyCategoryView(ModelView):
    column_searchable_list = ['id','name']
    column_filters = ['id','name']



admin = Admin(app, name="TTDHotel", template_mode="bootstrap4")

admin.add_view(MyCategoryView(Category, db.session))


if __name__ == "__main__":
    app.run(debug=True)