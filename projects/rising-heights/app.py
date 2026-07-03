from flask import Blueprint, render_template

blueprint = Blueprint("blueprint", __name__, template_folder='game', static_folder='game', static_url_path='')

@blueprint.route("/")
def index():
    return render_template("RisingHeights.html")
