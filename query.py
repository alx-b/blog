import datetime

from flask import session, flash
import argon2

from model import User, Post

# def save_user(name, password):
#    user = User(username=name, password=password)
#    user.save()
#
#
def save_post(title, text, user_id):
    print(datetime.datetime.now().strftime("%d/%m/%Y - %X"))
    post = Post(
        title=title,
        text=text,
        user_id=user_id,
        date_posted=datetime.datetime.now().strftime("%d/%m/%Y - %X"),
    )
    post.save() if post else flash("Couldn't save the post")


def get_posts_in_descending_order():
    try:
        posts = Post.select(Post, User).join(User).order_by(Post.date_posted.desc())
        return posts if posts else flash("No post yet!")
    except:
        flash("Couldn't get posts, something went wrong")
        return None


def get_post_by_id(post_id):
    try:
        post = Post.select(Post, User).join(User).where(Post.id == post_id).get()
        return post if post else flash("No post yet!")
    except:
        flash("Couldn't get the post, something went wrong")
        return None


def authorize_user(user):
    try:
        session["user_id"] = user.id
        session["username"] = user.username
        flash("Succesfully logged in!")
    except:
        flash("Something went wrong!")


def confirm_login(form_username, form_password):
    try:
        user = User.select().where(User.username == form_username).get()
        argon2.PasswordHasher().verify(user.password, form_password)
        authorize_user(user)
        if argon2.PasswordHasher().check_needs_rehash(user.password):
            print("password needs a rehash!")
            # Might need to auto-rehash and update database?
    except:
        flash("Wrong authentifications!")


def confirm_signup(username, password, confirm):
    if username_is_unique(username):
        try:
            hashed_password = get_hashed_password(password)
            user = add_and_return_a_user(username, hashed_password)
            authorize_user(user)
            flash("Account created!")
        except:
            flash("Something went wrong!")
    else:
        flash("Username already exists.")


def get_hashed_password(password):
    return argon2.PasswordHasher().hash(password)


def clear_session():
    session.clear()
    flash("Sucessfully logged out!")


def user_is_logged_in():
    return True if session.get("user_id") else False


def get_current_user():
    if user_is_logged_in():
        return User.get(User.id == session["user_id"])


def username_is_unique(username):
    return not User.select().where(User.username == username).exists()


def add_and_return_a_user(username, password):
    try:
        user = User.create(username=username, password=password)
        return user
    except:
        flash("Couldn't create user!")
        return None
