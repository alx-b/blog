from flask import render_template, Blueprint

errors = Blueprint(
    "errors", __name__, static_folder="static", template_folder="templates"
)


@errors.app_errorhandler(404)
def error_404(error):
    return render_template("404.html"), 404


@errors.app_errorhandler(403)
def error_403(error):
    return render_template("403.html"), 403


@errors.app_errorhandler(500)
def error_500(error):
    return render_template("500.html"), 500
