from flask import Blueprint, jsonify, session, g, request
from src.models import Player
# from src.extension import db
from datetime import datetime
from src.extension import get_db_connection

bp_player = Blueprint("players_info", __name__, url_prefix="/player")


@bp_player.route("/get_players", methods=['GET'])
def get_players():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM player ORDER BY last_name ASC, birthdate DESC"
            cursor.execute(sql)
            players = cursor.fetchall()
            return jsonify(players)
    except Exception as e:
        return jsonify({'status': 'failure', 'message': str(e)}), 500
    finally:
        connection.close()


@bp_player.route("/get_teams", methods=['GET'])
def get_teams():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "SELECT id, abbreviation FROM team"
            cursor.execute(sql)
            players = cursor.fetchall()
            return jsonify(players)
    except Exception as e:
        return jsonify({'status': 'failure', 'message': str(e)}), 500
    finally:
        connection.close()

