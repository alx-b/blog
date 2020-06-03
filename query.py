import datetime

from flask import flash

from model import User, Post


def stringify_date(dt_object):
    return dt_object.strftime("%d/%m/%Y - %X")


def get_total_pages(posts_per_page):
    posts = Post.select().order_by(Post.date_posted.desc())
    total_pages = int((len(posts) / posts_per_page) + (len(posts) % posts_per_page))
    return total_pages if total_pages > 0 else 1


# POST
def save_post(title, text, user_id):
    post = Post(
        title=title, text=text, user_id=user_id, date_posted=datetime.datetime.now()
    )
    post.save() if post else flash("Couldn't save the post")


def get_post_by_id(post_id):
    """Get data from database and return it as Post instance."""
    try:
        post = Post.select(Post, User).join(User).where(Post.id == post_id).get()
        return post if post else flash("No post yet!")
    except:
        flash("Couldn't get the post, something went wrong")
        return None


def update_post(post_id, title, text):
    try:
        (
            Post.update(title=title, text=text, last_updated=datetime.datetime.now())
            .where(Post.id == post_id)
            .execute()
        )
        flash("Post updated!")
    except:
        flash("Couldn't update the post!")


def delete_post(post_id):
    try:
        Post.delete().where(Post.id == post_id).execute()
        flash("Post deleted!")
    except:
        flash("Couldn't delete the post!")


def get_posts_in_descending_order(page, posts_per_page):
    """Return a list instance of all posts in descending order by date."""
    posts = (
        Post.select(Post, User)
        .join(User)
        .order_by(Post.date_posted.desc())
        .paginate(page, posts_per_page)
    )
    return posts if posts else flash("No post yet!")


# USER
def add_and_return_a_user(username, password):
    """Add data to database and return it as User instance."""
    try:
        user = User.create(username=username, password=password)
        return user
    except:
        flash("Couldn't create user!")
        return None
