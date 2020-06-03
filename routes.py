import functools

from flask import render_template, request, redirect, url_for, Blueprint, flash, abort

import query
import forms
import auth

routes = Blueprint(
    "routes", __name__, static_folder="static", template_folder="templates"
)


def login_required(func):
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        if not auth.user_is_logged_in():
            return redirect(url_for("routes.login"))
            # return redirect(url_for('auth.login', next=request.url))
        return func(*args, **kwargs)

    return decorated_function


@routes.route("/", defaults={"page": 1}, methods=["GET", "POST"])
@routes.route("/<int:page>", methods=["GET", "POST"])
def index(page):
    return render_template("index.html")


@routes.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


@routes.route("/testing", methods=["GET"])
def testing():
    query.main()
    return render_template("testing.html")


@routes.route("/post/all/page/", defaults={"page": 1}, methods=["GET"])
@routes.route("/post/all/page/<int:page>", methods=["GET"])
def posts(page):
    try:
        posts_per_page = 6
        posts = query.get_posts_in_descending_order(page, posts_per_page)
        total_pages = query.get_total_pages(posts_per_page)
        return render_template(
            "posts.html", page=page, posts=posts, total_pages=total_pages
        )
    except:
        abort(404)


@routes.route("/post/new", methods=["GET", "POST"])
@login_required
def create_post():
    form = forms.ComposePostForm()
    if form.validate_on_submit():
        try:
            query.save_post(form.title.data, form.text.data, auth.get_current_user().id)
            return redirect(url_for("routes.posts"))
        except:
            flash("Something went wrong!")
    return render_template("create_post.html", form=form)


@routes.route("/post/<int:id>", methods=["GET", "POST"])
def read_post(id):
    try:
        post = query.get_post_by_id(id)
        return render_template("post.html", id=id, post=post)
    except:
        abort(404)


@routes.route("/post/<int:id>/update", methods=["GET", "POST"])
@login_required
def update_post(id):
    form = forms.ComposePostForm()
    post = query.get_post_by_id(id)
    if post.user_id.id == auth.get_current_user().id:
        if form.validate_on_submit():
            try:
                # query.update_post(id, form.title.data, form.text.data)
                query.update_post(id, form.title.data, form.text.data)
                return redirect(url_for("routes.posts"))
            except:
                flash("Something went wrong!")
        form.title.data = post.title
        form.text.data = post.text
        return render_template("update_post.html", id=id, form=form)
    else:
        abort(403)


@routes.route("/post/<int:id>/delete", methods=["GET"])
@login_required
def delete_post(id):
    post = query.get_post_by_id(id)
    if post.user_id.id == auth.get_current_user().id:
        try:
            query.delete_post(id)
            return redirect(url_for("routes.posts"))
        except:
            flash("Something went wrong!")
            abort(500)
    else:
        abort(403)


@routes.route("/signup", methods=["GET", "POST"])
def signup():
    if auth.user_is_logged_in():
        flash("You are already logged in!")
        return redirect(url_for("routes.index"))
    form = forms.RegisterForm()
    if form.validate_on_submit():
        try:
            if auth.confirm_signup(
                form.username.data, form.password.data, form.confirm_password.data
            ):
                return redirect(url_for("routes.posts"))
        except:
            flash("Something went wrong!")
    return render_template("signup.html", form=form)


@routes.route("/login", methods=["GET", "POST"])
def login():
    if auth.user_is_logged_in():
        flash("You are already logged in!")
        return redirect(url_for("routes.index"))
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            if auth.confirm_login(form.username.data, form.password.data):
                return redirect(url_for("routes.posts"))
        except:
            flash("Something went wrong")
    return render_template("login.html", form=form)


@routes.route("/logout", methods=["GET"])
@login_required
def logout():
    auth.clear_session()
    return redirect(url_for("routes.login"))
