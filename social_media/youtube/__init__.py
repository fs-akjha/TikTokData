from datetime import timedelta

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

app = Flask(__name__)
ma = Marshmallow(app)

app.config['SECRET_KEY']='thisissecret'
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.config['YOUTUBE_API_KEY']='AIzaSyBjXk8xwQorp3I_qlFEUHT022BnR2EkHgk'

jwt_manager = JWTManager(app)

from app import user_views
from app import campaign_views
from app import social_media_views
