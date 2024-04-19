from flask import Flask, request, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import User
from src.extension import db
from resource import config
from flask_session import Session
from src.blueprints.auth import bp


app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)

SESSION_TYPE = 'memcache'
sess = Session()
sess.init_app(app)

app.register_blueprint(bp)


# @app.route('/add/user', methods=['POST'])
# def add_user():
#     response_object = {'status': 'success'}
#     name = request.json.get("name")
#     password = request.json.get("password")
#     email = request.json.get("email")
#     user = User(name=name, password=password, email=email)
#     db.session.add(user)
#     db.session.commit()
#     return jsonify(response_object)

