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
    return render_template("testing.html", films=query.something())


# @routes.route("/post/all/page/", defaults={"page": 1}, methods=["GET"])
@routes.route("/post/all/page/<int:page>", defaults={"page": 1}, methods=["GET"])
def posts(page):
    return render_template("posts.html", page=page)


@routes.route("/post/new", methods=["GET", "POST"])
def create_post():
    form = forms.ComposePostForm()
    return render_template("create_post.html", form=form)


@routes.route("/post/<int:id>", methods=["GET", "POST"])
def read_post(id):
    pass


@routes.route("/post/<int:id>/update", methods=["GET", "POST"])
def update_post(id):
    pass


@routes.route("/post/<int:id>/delete", methods=["GET", "POST"])
def delete_post(id):
    pass


@routes.route("/signup", methods=["GET", "POST"])
def signup():
    return render_template("signup.html")


@routes.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


@routes.route("/logout", methods=["GET", "POST"])
def logout():
    pass
