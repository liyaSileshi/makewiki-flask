from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from makewiki import db, bcrypt
from makewiki.models import User, Post
from makewiki.users.forms import (RegistrationForm, LoginForm, 
                            RequestResetForm, ResetPasswordForm)
from makewiki.users.utils import send_reset_email

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    #hash the pw
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    #create a new instance of the user
    user = User(username=form.username.data, email=form.email.data, password=hashed_password)
    #add the user to db and commit
    db.session.add(user)
    db.session.commit()

    flash(f'Your account has been created! You are now able to log in', 'success')
    return redirect(url_for('users.login')) #redirect to login page
  return render_template('register.html', title='Register', form=form)

@users.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('main.home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      #log the user in
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      #redired to home after logging in or to the next page if it exists(eg: accounts)
      return redirect(next_page) if next_page else redirect(url_for('main.home')) 
    else:
      flash('Login Unsuccessful. Please check email and password', 'danger')
  return render_template('login.html', title='Login', form=form)

@users.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('main.home')) #redired to home after logging out

@users.route("/account")
@login_required
def account():
  return render_template('account.html', title='Account')

#forgot password routes
@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request(): #enter email to request password request
  if current_user.is_authenticated: #to make sure users are logged out before they reset their password
    return redirect(url_for('main.home'))
  form = RequestResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first() #grab the user with the email
    send_reset_email(user)
    flash('An email has been sent with instructions to reset your password.', 'info')
    return redirect(url_for('users.login'))
  return render_template('reset_request.html', title='Reset Password', form=form)
 
@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated: #to make sure users are logged out before they reset their password
    return redirect(url_for('main.home'))
  user = User.verify_reset_token(token)
  if not user: #if the token the user entered was invalid/expired
    flash('That is an invalid or expired token', 'warning')
    return redirect(url_for('users.reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    #hash the pw
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user.password = hashed_password
    #add and commit
    db.session.commit()

    flash(f'Your password has been updated! You are now able to log in', 'success')
    return redirect(url_for('users.login')) #redirect to login page
  return render_template('reset_token.html', title='Reset Password', form=form)