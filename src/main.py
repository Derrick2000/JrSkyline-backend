from flask import Flask
from src.extension import db
from src import config
from flask_session import Session
from src.blueprints.auth import bp
from src.blueprints.team import bp_team


app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)

sess = Session()
sess.init_app(app)

app.register_blueprint(bp)
app.register_blueprint(bp_team)



