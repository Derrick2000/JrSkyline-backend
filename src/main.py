from flask import Flask
from src.extension import db
from src import config
from flask_session import Session
from src.blueprints.auth import bp
from src.blueprints.player import bp_player
from src.blueprints.team import bp_team
from src.blueprints.game import bp_game
from src.blueprints.news import bpN

app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)

sess = Session()
sess.init_app(app)

app.register_blueprint(bp_player)
app.register_blueprint(bp)
app.register_blueprint(bp_team)
app.register_blueprint(bp_game)
app.register_blueprint(bpN)




