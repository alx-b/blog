import datetime

from flask import flash

from model import User, Post


def save_post(title, text, user_id):
    post = Post(
        title=title,
        text=text,
        user_id=user_id,
        date_posted=datetime.datetime.now().strftime("%d/%m/%Y - %X"),
    )
    post.save() if post else flash("Couldn't save the post")


def update_post(post_id, title, text):
    try:
        Post.update(title=title, text=text).where(Post.id == post_id).execute()
        flash("Post updated!")
    except:
        flash("Couldn't update the post!")


def delete_post(post_id):
    try:
        Post.delete().where(Post.id == post_id).execute()
        flash("Post deleted!")
    except:
        flash("Couldn't delete the post!")


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


def add_and_return_a_user(username, password):
    try:
        user = User.create(username=username, password=password)
        return user
    except:
        flash("Couldn't create user!")
        return None
