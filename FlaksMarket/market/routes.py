from market import app
from flask import render_template, redirect, url_for, flash, session
from market.models import Item, User
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')



@app.route('/market')
@login_required
def market_page():
    items = Item.query.all()
    return render_template('market.html',items=items)

@app.route("/register",methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,email_address=form.email_address.data,password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        session['logged_in'] = True
        session['username'] = form.username
        l = login_user(user_to_create)
        print('-----LOGIN USER-----',l)
        
        flash(f'Success! You are logged in as : {form.username.data}')
        #return redirect(url_for("market_page"))
        return render_template("market.html")
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f" There was an error with createing a user : {err_msg}")
    return render_template("register.html",form=form,category="danger")


@app.route('/login',methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_connection(attempted_password=form.password.data):
            session['logged_in'] = True
            session['username'] = attempted_user.username
            login_user(attempted_user)
            
            flash(f'Success! You are logged in as : {attempted_user.username}')
            return redirect(url_for("market_page"))
        else:
            flash("Username and password not match! Please try Again")
    return render_template("login.html",form=form)


@app.route('/logout')
def logout_page():
    session.clear()
    logout_user()
    flash("You have logged out!")
    return redirect(url_for("home_page"))
