from flask import Flask
from src.extension import db
from src import config
from flask_session import Session
from src.blueprints.auth import bp
from src.blueprints.player import bp_player


app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)

sess = Session()
sess.init_app(app)

app.register_blueprint(bp_player)
app.register_blueprint(bp)



