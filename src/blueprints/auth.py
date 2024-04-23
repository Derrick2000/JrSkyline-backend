from flask import Blueprint, jsonify, session, g, request
from src.models import User
from werkzeug.security import check_password_hash, generate_password_hash
# from src.extension import db
from datetime import datetime
from src.extension import get_db_connection

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

    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "select * from user where name = %s"
        cursor.execute(sql, username)
        user = cursor.fetchone()
        if user is None:
            response_object['status'] = 'failure'
            response_object['message'] = 'This user does not exist'
        elif not check_password_hash(user['password'], password):
            response_object['status'] = 'failure'
            response_object['message'] = 'Incorrect password'
        else:
            session.clear()
            user_id = user['id']
            session['user_id'] = user_id
            response_object['username'] = username
            response_object['user_id'] = user_id
    return jsonify(response_object)


@bp.route("/register", methods=['POST'])
def register():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        password_check = request.json.get('re_password')
        email = request.json.get('email')
        date = datetime.now()

        if password_check != password:
            response_object['status'] = 'failure'
            response_object['message'] = 'Password typed are not the same, try again'
            return jsonify(response_object)

        password = generate_password_hash(password)

        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "select id from user order by id desc limit 1"
            cursor.execute(sql)
            user_id = cursor.fetchone()['id'] + 1
            sql = "INSERT INTO user VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (user_id, username, email, password, date))
        connection.commit()
        session.clear()
        session['user_id'] = user_id
        response_object['user_id'] = user_id
        response_object['username'] = username
    return jsonify(response_object)


@bp.route("/logout", methods=['GET'])
def logout():
    response_object = {'status': 'success'}
    session.clear()
    return jsonify(response_object)

