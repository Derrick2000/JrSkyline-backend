from flask import Blueprint, jsonify, session, g, request
from models import User
from werkzeug.security import check_password_hash, generate_password_hash
from src.extension import db


bp = Blueprint("authorization", __name__, url_prefix="/auth")


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(int(user_id))


@bp.route("/login", methods=['POST'])
def login():
    response_object = {'status': 'success'}
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(name=username).first()
    if user is None:
        user = User.query.filter_by(email=username).first()
    if user is None:
        response_object['status'] = 'failure'
        response_object['message'] = 'This user does not exist'
        return response_object
    elif not check_password_hash(user.password, password):
        response_object['status'] = 'failure'
        response_object['message'] = 'Incorrect password'
        return jsonify(response_object)
    session.clear()
    session['user_id'] = user.id
    response_object['username'] = username
    response_object['user_id'] = user.id
    return jsonify(response_object)


@bp.route("/register", methods=['POST'])
def register():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        password_check = request.json.get('re_password')
        email = request.json.get('email')

        if password_check != password:
            response_object['status'] = 'failure'
            response_object['message'] = 'Password typed are not the same, try again'
            return jsonify(response_object)

        check_user = User.query.filter_by(name=username).first()
        if check_user:
            response_object['status'] = 'failure'
            response_object['message'] = 'Username existed, try another one'
            return jsonify(response_object)

        check_email = User.query.filter_by(email=email).first()
        if check_email:
            response_object['status'] = 'failure'
            response_object['message'] = 'Email existed, try another one'
            return jsonify(response_object)

        user = User(name=username, password=generate_password_hash(password), email=email)
        db.session.add(user)
        db.session.commit()
        session.clear()
        session['user_id'] = user.id
        response_object['user_id'] = user.id
        response_object['username'] = username
    return jsonify(response_object)


@bp.route("/logout", methods=['GET'])
def logout():
    session.clear()
    return None

