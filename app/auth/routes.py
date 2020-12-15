import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response
)
from flask_login import current_user, login_user, logout_user
from flask_api import status
from flask_cors import CORS, cross_origin
from werkzeug.urls import url_parse
import json

from app import db, cache
from app.models import User
from app.auth import bp
from app.auth.forms import LoginForm, RegistrationForm

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=form)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('auth/login.html', title='Sign In', form=form)

@bp.route('/api_login', methods=('GET', 'POST'))
@cross_origin()
def api_login():
    if current_user.is_authenticated:
        return current_user

    data = json.loads(request.data.decode("utf-8"))
    username = data["username"]
    password = data["password"]
    if username != "" and password != "":
        user = User.query.filter_by(username = username).first()
        if user is None:
            return make_response(
                "{'user':'" + str(username) + "'}",
                status.HTTP_404_NOT_FOUND,
                {"Content-Type": "application/json"})
        if not user.check_password(password):
            return make_response(
                "{'password':'wrong'}",
                status.HTTP_404_NOT_FOUND,
                {"Content-Type": "application/json"})

        login_user(user)
        return make_response(
            user.jsonify(),
            status.HTTP_200_OK,
            {"Content-Type": "application/json"})

    return make_response(
        "{}",
        status.HTTP_401_UNAUTHORIZED,
        {"Content-Type": "application/json"})

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
