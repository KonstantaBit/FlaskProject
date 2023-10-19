from flask import session, flash
from models import User


def auth_user(user):
    session['logged_in'] = True
    session['user_id'] = user.id
    session['username'] = user.username
    flash('You are logged in as %s' % (user.username))


def get_current_user():
    if session.get('logged_in'):
        return User.get(User.id == session['user_id'])
