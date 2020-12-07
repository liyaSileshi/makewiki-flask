import os

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY')
  SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
  MAIL_SERVER = 'smtp.googlemail.com' #for password reset
  MAIL_PORT = 587 #for password reset
  MAIL_USE_TLS = True #for password reset
  MAIL_USERNAME = os.environ.get('EMAIL_USER') #for password reset
  MAIL_PASSWORD = os.environ.get('EMAIL_PASS') #for password reset
