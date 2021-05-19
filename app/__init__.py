from datetime import timedelta
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from gevent import monkey
monkey.patch_all()

app = Flask(__name__)
monkey.patch_all()
ma = Marshmallow(app)

app.config['SECRET_KEY']='thisissecret'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config['YOUTUBE_API_KEY']='AIzaSyDWAmLd4oAT85ufTNvHFqu-FCcHRyUt59c'

jwt_manager = JWTManager(app)

from app import user_views
from app import campaign_views
# from app import social_media_views
