from flask import Blueprint, flash, session
import argon2

from model import User
import query


def user_is_logged_in():
    return True if session.get("user_id") else False


def get_current_user():
    if user_is_logged_in():
        return User.get(User.id == session["user_id"])


def authorize_user(user):
    try:
        session["user_id"] = user.id
        session["username"] = user.username
        flash("Succesfully logged in!")
    except:
        flash("Something went wrong!")


def clear_session():
    session.clear()
    flash("Sucessfully logged out!")


def confirm_login(form_username, form_password):
    try:
        user = User.select().where(User.username == form_username).get()
        argon2.PasswordHasher().verify(user.password, form_password)
        authorize_user(user)
        if argon2.PasswordHasher().check_needs_rehash(user.password):
            print("password needs a rehash!")
        return True
        # Might need to auto-rehash and update database?
    except:
        flash("Wrong authentifications!")
        return False


def confirm_signup(username, password, confirm):
    if username_is_unique(username):
        try:
            hashed_password = get_hashed_password(password)
            user = query.add_and_return_a_user(username, hashed_password)
            authorize_user(user)
            flash("Account created!")
            return True
        except:
            flash("Something went wrong!")
            return False
    else:
        flash("Username already exists.")
        return False


def get_hashed_password(password):
    return argon2.PasswordHasher().hash(password)


def username_is_unique(username):
    return not User.select().where(User.username == username).exists()
