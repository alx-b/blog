from flask import render_template, request, redirect, url_for, Blueprint, flash
import functools
import query
import forms

routes = Blueprint(
    "routes", __name__, static_folder="static", template_folder="templates"
)


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


# @routes.route("/post/all/page/", defaults={"page": 1}, methods=["GET"])
@routes.route(
    "/post/all/page/<int:page>", defaults={"page": 1}, methods=["GET", "POST"]
)
def posts(page):
    posts = query.get_posts_in_descending_order()
    if posts:
        return render_template("posts.html", page=page, posts=posts)
    return render_template("posts.html", page=page)


@routes.route("/post/new", methods=["GET", "POST"])
def create_post():
    form = forms.ComposePostForm()
    if form.validate_on_submit():
        query.save_post(form.title.data, form.text.data, query.get_current_user().id)
        return redirect(url_for("routes.posts"))
    return render_template("create_post.html", form=form)


@routes.route("/post/<int:id>", methods=["GET", "POST"])
def read_post(id):
    post = query.get_post_by_id(id)
    if post:
        return render_template("post.html", id=id, post=post)
    return render_template("post.html", id=id)


@routes.route("/post/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    pass


@routes.route("/post/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    pass


@routes.route("/signup", methods=["GET", "POST"])
def signup():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        query.confirm_signup(
            form.username.data, form.password.data, form.confirm_password.data
        )
    return render_template("signup.html", form=form)


@routes.route("/login", methods=["GET", "POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            query.confirm_login(form.username.data, form.password.data)
            return redirect(url_for("routes.posts"))
        except:
            flash("Something went wrong")

    return render_template("login.html", form=form)


@routes.route("/logout", methods=["GET", "POST"])
def logout():
    query.clear_session()
    return redirect(url_for("routes.login"))
