from flask import render_template, url_for, flash, redirect, request
from soltrade import app, db, bcrypt
from soltrade.forms import RegistrationForm, LoginForm
from soltrade.models import User, Post
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
                user = User(username=form.username.data, email=form.email.data, password=hashed_password)
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

@app.route("/account")
@login_required
def account():
        return render_template('account.html', title='Account')