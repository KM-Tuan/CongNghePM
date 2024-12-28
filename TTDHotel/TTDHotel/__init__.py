from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import  cloudinary, os
from authlib.integrations.flask_client import OAuth



app = Flask(__name__, template_folder="templates")

app.secret_key = 'secret_key'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/hoteldb?charset=utf8mb4" % quote('Admin@123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config['PAGE_SIZE'] = 8
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

db = SQLAlchemy(app)


cloudinary.config(
    cloud_name= 'dqpoa9ukn',
    api_key= '899116174815345',
    api_secret= 'vIvSb9Qf-mMqCoopdkgEVgfRDMw',
)

# Truy xuất giá trị môi trường

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id="294714413960-kceqf54eu6rrkh9af98pj9n5ehtmpf8q.apps.googleusercontent.com",
    client_secret="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",
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'email profile'},
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

# Cấu hình Facebook OAuth
facebook = oauth.register(
    name='facebook',
    client_id="962541772387140",
    client_secret="1cb70175dd12e7c2ea950b26cd3fe684",
    access_token_url='https://graph.facebook.com/v12.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v12.0/dialog/oauth',
    api_base_url='https://graph.facebook.com/v12.0/',
    client_kwargs={'scope': 'email'}
)