from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from TTDHotel.TTDHotel import app, db
from models import Category, Account, RoomStatus, CustomerType, StatusAccount, Role, Employee, Customer, Room, RoomBooked, RoomRented, Bill, BookingDetail, RentingDetail

from flask_login import current_user, login_user, logout_user


class MyCategoryView(ModelView):
    column_searchable_list = ['id','name']
    column_filters = ['id','name']



admin = Admin(app, name="TTDHotel", template_mode="bootstrap4")

# admin.add_view(MyCategoryView(Category, db.session))

class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 1


admin.add_view(AuthenticatedView(Account, db.session, category='Quản lý tài khoản'))
admin.add_view(AuthenticatedView(Customer, db.session, category='Quản lý khách hàng'))
admin.add_view(AuthenticatedView(RoomStatus, db.session, category='Quản lý phòng'))
admin.add_view(AuthenticatedView(CustomerType, db.session, category='Quản lý khách hàng'))
admin.add_view(AuthenticatedView(StatusAccount, db.session, category='Quản lý tài khoản'))
admin.add_view(AuthenticatedView(Role, db.session, category='Quản lý tài khoản'))
admin.add_view(AuthenticatedView(Category, db.session, category='Quản lý phòng'))
admin.add_view(AuthenticatedView(Employee, db.session, category='Quản lý nhân sự'))
admin.add_view(AuthenticatedView(Room, db.session, category='Quản lý phòng'))
admin.add_view(AuthenticatedView(RoomBooked, db.session, category='Quản lý đặt phòng'))
admin.add_view(AuthenticatedView(BookingDetail, db.session, category='Quản lý đặt phòng'))
admin.add_view(AuthenticatedView(RoomRented, db.session, category='Quản lý thuê phòng'))
admin.add_view(AuthenticatedView(RentingDetail, db.session, category='Quản lý thuê phòng'))
admin.add_view(AuthenticatedView(Bill, db.session, category='Quản lý hóa đơn'))

if __name__ == "__main__":
    app.run(debug=True)