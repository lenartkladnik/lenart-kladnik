import os
import sys
from flask import Blueprint, abort, render_template

def load_project(name: str) -> Blueprint:
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), name))

    blueprint = __import__("app").blueprint

    def _readme():
        path = os.path.join(os.path.dirname(__file__), name, "README.html")
        if os.path.exists(path):
            return render_template(f"/{name}/README.html")
        return abort(404)

    blueprint.add_url_rule("/README", f"_readme_{name}", _readme)

    return blueprint

projects = Blueprint("projects", __name__, template_folder='.', static_folder='.')

projects.register_blueprint(load_project("rising-heights"), url_prefix="/rising-heights")
