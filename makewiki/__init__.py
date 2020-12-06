import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail #for forgot pw


app = Flask(__name__)
app.config['SECRET_KEY'] = '890e039fefda66fb75b9eddbf1daedae'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #function name of the login route, redirects user to this page if not authenticated
login_manager.login_message_category = 'info' #bootstrap class for alert login
app.config['MAIL_SERVER'] = 'smtp.googlemail.com' #for password reset
app.config['MAIL_PORT'] = 587 #for password reset
app.config['MAIL_USE_TLS'] = True #for password reset
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER') #for password reset
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS') #for password reset

mail = Mail(app)
from makewiki import routes