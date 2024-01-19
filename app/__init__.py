from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
from flask_login import LoginManager
from flask_admin import Admin

app = Flask(__name__)
app.secret_key = '23823^%&*(*^^%^&%^&$%$&&'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/plane_db?charset=utf8mb4' % quote('Anhquoc@2476')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

login = LoginManager(app=app)