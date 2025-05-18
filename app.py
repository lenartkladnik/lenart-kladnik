from flask import Flask, Blueprint
from waitress import serve
from views import views
<<<<<<< HEAD

app = Flask(__name__)

=======
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def inject():
    return dict(year=datetime.now().year)

>>>>>>> e5ba943 (Major UI update.)
app.register_blueprint(views, url_prefix="/")

if __name__ == '__main__':
    serve(app, port='5002', threads=6)
