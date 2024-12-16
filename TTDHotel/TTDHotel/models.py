from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from TTDHotel.TTDHotel import app, db


class Category(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    with app.app_context():
        # db.create_all()
        c = Category(name="Phòng VIP")
        db.session.add(c)
        db.session.commit()
