from flask import render_template, url_for, flash, redirect, request, abort
from makewiki.forms import (RegistrationForm, LoginForm, PostForm, 
                          RequestResetForm, ResetPasswordForm)
from makewiki.models import User, Post
from makewiki import app, db, bcrypt, mail
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

@app.route("/")
@app.route("/home")
def home():
  posts = Post.query.all() #get all posts
  return render_template('home.html', posts=posts)

@app.route("/about")
def about():
  return render_template('about.html', title="About")

@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
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
    return redirect(url_for('login')) #redirect to login page
  return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user and bcrypt.check_password_hash(user.password, form.password.data):
      #log the user in
      login_user(user, remember=form.remember.data)
      next_page = request.args.get('next')
      #redired to home after logging in or to the next page if it exists(eg: accounts)
      return redirect(next_page) if next_page else redirect(url_for('home')) 
    else:
      flash('Login Unsuccessful. Please check email and password', 'danger')
  return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home')) #redired to home after logging out

@app.route("/account")
@login_required
def account():
  return render_template('account.html', title='Account')

#create a new post
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
  form = PostForm()
  if form.validate_on_submit():
    #create a post instance
    post = Post(title=form.title.data, content=form.content.data, author=current_user)
    #add and save to db
    db.session.add(post)
    db.session.commit()

    flash('Your post has been created!', 'success')
    return redirect(url_for('home'))
  return render_template('create_post.html', title='New Post', 
                        form=form, legend='New Post')

#display a single post
@app.route("/post/<int:post_id>")
def post(post_id):
  post = Post.query.get_or_404(post_id)
  return render_template('post.html', title=post.title, post=post)

#update a post
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403) #return an error 'forbidden route'
  form = PostForm() #else get the post form

  #post request
  if form.validate_on_submit():
    post.title = form.title.data
    post.content = form.content.data
    db.session.commit() #commit your change
    flash('Your post has been updated', 'success')
    return redirect(url_for('post', post_id=post.id))
  #get request
  elif request.method == 'GET': 
    #populate form with title and content
    form.title.data = post.title 
    form.content.data = post.content
  return render_template('create_post.html', title='Update Post', 
                        form=form, legend='Update Post')

#delete a post
@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
  post = Post.query.get_or_404(post_id)
  if post.author != current_user:
    abort(403) #return an error 'forbidden route'
  #delete the post
  db.session.delete(post)
  db.session.commit()
  flash('Your post has been deleted!', 'success')
  return redirect(url_for('home'))


def send_reset_email(user):
  token = user.get_reset_token()
  msg = Message('Password Reset Request', 
                sender='noreply@demo.com', 
                recipients=[user.email])
  msg.body  = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
  #send the message
  mail.send(msg)

#forgot password routes
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request(): #enter email to request password request
  if current_user.is_authenticated: #to make sure users are logged out before they reset their password
    return redirect(url_for('home'))
  form = RequestResetForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first() #grab the user with the email
    send_reset_email(user)
    flash('An email has been sent with instructions to reset your password.', 'info')
    return redirect(url_for('login'))
  return render_template('reset_request.html', title='Reset Password', form=form)
 
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
  if current_user.is_authenticated: #to make sure users are logged out before they reset their password
    return redirect(url_for('home'))
  user = User.verify_reset_token(token)
  if not user: #if the token the user entered was invalid/expired
    flash('That is an invalid or expired token', 'warning')
    return redirect(url_for('reset_request'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    #hash the pw
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user.password = hashed_password
    #add and commit
    db.session.commit()

    flash(f'Your password has been updated! You are now able to log in', 'success')
    return redirect(url_for('login')) #redirect to login page
  return render_template('reset_token.html', title='Reset Password', form=form)