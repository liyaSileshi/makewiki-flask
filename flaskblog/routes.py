from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog.forms import RegistrationForm, LoginForm, PostForm
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required


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
