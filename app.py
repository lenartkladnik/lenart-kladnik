import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "projects")) # For from projects import projects

from flask import Flask
from waitress import serve
from views import views
from projects import projects
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def inject():
    return dict(year=datetime.now().year)

app.register_blueprint(views, url_prefix="/")
app.register_blueprint(projects, url_prefix="/projects")

if __name__ == '__main__':
    serve(app, port='5002', threads=6)
