import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from soltrade import app, db, bcrypt
from soltrade.forms import RegistrationForm, LoginForm, UpdateAccountForm
from soltrade.models import User, Post, Group
from flask_login import login_user, current_user, logout_user, login_required
from soltrade.microgrid import MicroGrid

num_prosumers = 5
internal_price = 4
external_price = 6
microgrid = MicroGrid(num_prosumers, internal_price, external_price)

@app.route("/")
@app.route("/home")
def home():
        return render_template('home.html')

@app.route("/about")
def about():
        return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
        if current_user.is_authenticated:
                return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
                # making new user for db
                print("TESTING")
                print(form.group.data)
                user_group = Group.query.filter_by(groupname=form.group.data).first()
                user = User(username=form.username.data, email=form.email.data, password=hashed_password, group=user_group)
                db.session.add(user)
                db.session.commit()
                flash(f'An account was created for {form.username.data} --- you can now log in!', 'success')
                return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
        if current_user.is_authenticated:
                return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
                user = User.query.filter_by(email=form.email.data).first()
                if user and bcrypt.check_password_hash(user.password, form.password.data):
                        login_user(user, remember=form.remember.data)
                        next_page = request.args.get('next')
                        flash('You\'ve been logged in!', 'success')
                        return redirect(next_page) if next_page else redirect(url_for('home'))
                else:
                        flash('Login unsuccessful -- please check email and password.', 'danger')
        return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
        logout_user()
        return redirect(url_for('home'))

def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        f_ext = os.path.splitext(form_picture.filename)[1]
        pic_fn = random_hex + f_ext
        pic_path = os.path.join(app.root_path, 'static/img/profilepics', pic_fn)
        output_size = (250, 250)
        pic_resize = Image.open(form_picture)
        pic_resize.thumbnail(output_size)
        pic_resize.save(pic_path)
        return pic_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
        form = UpdateAccountForm()
        if form.validate_on_submit():
                if form.pic.data:
                        pic_file = save_picture(form.pic.data)
                        current_user.image_file = pic_file
                current_user.username = form.username.data
                current_user.email = form.email.data
                db.session.commit()
                flash('Your account has been updated!', 'success')
                return redirect(url_for('account'))
        elif request.method == 'GET':
                form.username.data = current_user.username
                form.email.data = current_user.email
        image_file = url_for('static', filename='img/profilepics/' + current_user.image_file)
        return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/grid", methods=['GET', 'POST'])
@login_required
def grid():
        return render_template('grid.html', title='Grid')