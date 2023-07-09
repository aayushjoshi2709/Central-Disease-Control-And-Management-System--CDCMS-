from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_apscheduler import APScheduler
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cdcms.db'
app.config['SECRET_KEY'] = '9f479d5aebc024b17588bd87'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
login_manager = LoginManager(app)
login_manager.login_view = 'home_page'
login_manager.login_message_category = 'info'
from cdcms import routes