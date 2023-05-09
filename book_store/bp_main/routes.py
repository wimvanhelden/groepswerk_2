from flask import render_template, Blueprint

bp_main = Blueprint('bp_main', __name__)


@bp_main.route("/home")
@bp_main.route("/")
def home():
    return render_template("home.html")


@bp_main.route("/about")
def about():
    return render_template("about.html")