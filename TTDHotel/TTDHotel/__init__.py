from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote

app = Flask(__name__, template_folder="templates")
app.secret_key = 'secret_key'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/hoteldb?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 2
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'


db = SQLAlchemy(app)