from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail #for forgot pw
from makewiki.config import Config #for configs

#initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' #function name of the login route, redirects user to this page if not authenticated
login_manager.login_message_category = 'info' #bootstrap class for alert login
mail = Mail()


#function for creation of our app
def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config) 

  db.init_app(app)
  bcrypt.init_app(app)
  login_manager.init_app(app)
  mail.init_app(app)

  #import blueprints
  from makewiki.users.routes import users
  from makewiki.posts.routes import posts
  from makewiki.main.routes import main
  #register blueprints
  app.register_blueprint(users)
  app.register_blueprint(posts)
  app.register_blueprint(main) 

  return app