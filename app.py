from flask import Flask

from models import bp

app = Flask(__name__)
app.register_blueprint(bp)
