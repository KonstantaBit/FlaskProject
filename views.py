from app import app, database
from auth import auth_user
from models import User, Post
from flask import request, render_template, redirect, flash, url_for, session, g
from peewee import IntegrityError
from hashlib import md5
from decorators import login_required
from auth import get_current_user
import datetime


#  ==== Работа с БД ====

@app.before_request
def before_request():
    g.db = database
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


#  ==== Работа с аунтификацией ====

@app.route('/join/', methods=['GET', 'POST'])
def join():
    if request.method == 'POST' and request.form['username']:
        try:
            with database.atomic():
                #  Пытаемся создать пользователя, если имя неуникально, то делаем исключение
                user = User.create(
                    username=request.form['username'],
                    password=md5((request.form['password']).encode('utf-8')).hexdigest(),
                    email=request.form['email'],
                    join_date=datetime.datetime.now())
            auth_user(user)
            return redirect(url_for('homepage'))

        except IntegrityError:
            flash('Этот юзернейм уже занят')

    return render_template('join.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['username']:
        try:
            pw_hash = md5(request.form['password'].encode('utf-8')).hexdigest()
            user = User.get(
                (User.username == request.form['username']) &
                (User.password == pw_hash))
        except User.DoesNotExist:
            flash('The password entered is incorrect')
        else:
            auth_user(user)
            return redirect(url_for('homepage'))

    return render_template('login.html')


@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('homepage'))


#  ==== Основные страницы ====

@app.route('/')
def homepage():
    posts = Post.select().order_by(Post.pub_date.desc())
    print(posts)
    return render_template('homepage.html', posts=posts)


@app.route('/create/', methods=['GET', 'POST'])
@login_required
def create():
    user = get_current_user()
    if request.method == 'POST' and request.form['content']:
        message = Post.create(
            user=user,
            content=request.form['content'],
            pub_date=datetime.datetime.now())
        flash('Your message has been created')
        return redirect(url_for('homepage'))

    return render_template('create.html')