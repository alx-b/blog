from flask import session, flash
from model import User, Post

# def save_user(name, password):
#    user = User(username=name, password=password)
#    user.save()
#
#
# def save_post(title, text, user_id, date):
#    post = Post(title=title, text=text, user_id=user_id, date_posted=date)
#    post.save()


def get_posts_in_descending_order():
    try:
        posts = Post.select(Post, User).join(User).order_by(Post.date_posted.desc())
        if posts:
            return posts
        else:
            flash("No post yet!")
    except:
        flash("Couldn't get posts, something went wrong")
        return None


def get_post_by_id(post_id):
    try:
        post = Post.select(Post, User).join(User).where(Post.id == post_id).get()
        if post:
            return post
        else:
            flash("No post yet!")
    except:
        flash("Couldn't get the post, something went wrong")
        return None
