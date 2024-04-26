from flask import Blueprint, jsonify, session, g, request
from src.models import Player
# from src.extension import db
from datetime import datetime
from src.extension import get_db_connection
import re

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


@bp_player.route("/add_player", methods=['POST'])
def add_player():
    birthdate_pattern = r'^\d{4}-\d{2}-\d{2}$'
    height_pattern = r'^\d+-\d+$'
    weight_pattern = r'^[1-9]\d*$'

    response_success = {'status': 'success'}
    response_failed = {'status': 'failed'}
    success = True
    connection = get_db_connection()
    first_name = request.json.get("first_name").capitalize()
    last_name = request.json.get("last_name").capitalize()
    birthdate = request.json.get("birthdate")
    country = request.json.get("country")
    height = request.json.get("height").replace("'", "-").replace('"', '')
    weight = str(request.json.get("weight"))
    position = request.json.get("position").capitalize()
    team_abbreviation: str = request.json.get("team_abbreviation").upper()
    cursor = connection.cursor()
    print(f"Player add - data set")
    try:
        if not re.match(birthdate_pattern, birthdate):
            raise ValueError(f"birthdate {birthdate} not valid (yyyy-mm-dd)")
        if not re.match(height_pattern, height):
            raise ValueError(f"height {height} not valid (feet\'inches\")")
        if not re.match(weight_pattern, weight):
            raise ValueError(f"weight {weight} not valid (int)")
        if (not first_name) or (not last_name) or (not country) or (not position):
            raise ValueError(f"values missing")
        print(f"Player add - data check")

        cursor.execute("select id from player order by id desc limit 1")
        player_id = cursor.fetchone()['id'] + 1
        cursor.execute("SELECT id FROM team WHERE abbreviation = %s", (team_abbreviation,))
        team_id = cursor.fetchone()['id']
        if team_id is None:
            raise ValueError(f"Team {team_abbreviation} not found")
        cursor.execute(
            "insert into player values(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (player_id, first_name, last_name, birthdate, country, height, weight, position, team_id)
        )
        connection.commit()
        print(f"Player add - success")
    except Exception as e:
            connection.rollback()
            print(f"Failed to add player: {e}")
            success = False
    finally:
        cursor.close()
    if success:
        return jsonify(response_success)
    return jsonify(response_failed), 500

@bp_player.route("/delete_player/<int:id>", methods=['POST'])
def delete_player(id):
    response_object = {'status': 'success'}
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "delete from player where id = %s"
            cursor.execute(sql, id)
        connection.commit()
        print("player delete success")
    except Exception as e:
        connection.rollback()
        print(f"Failed to delete player: {e}")
    return jsonify(response_object)



@bp_player.route("/edit_player/<int:id>", methods=['POST'])
def edit_player(id):
    birthdate_pattern = r'^\d{4}-\d{2}-\d{2}$'
    height_pattern = r'^\d+-\d+$'
    weight_pattern = r'^[1-9]\d*$'

    response_success = {'status': 'success'}
    response_failed = {'status': 'failed'}
    success = True
    connection = get_db_connection()
    first_name = request.json.get("first_name").capitalize()
    last_name = request.json.get("last_name").capitalize()
    birthdate = request.json.get("birthdate")
    country = request.json.get("country")
    height = request.json.get("height").replace("'", "-").replace('"', '')
    weight = str(request.json.get("weight"))
    position = request.json.get("position").capitalize()
    team_abbreviation: str = request.json.get("team_abbreviation").upper()
    cursor = connection.cursor()
    print(f"Player edit - data set")
    try:
        if not re.match(birthdate_pattern, birthdate):
            raise ValueError(f"birthdate {birthdate} not valid (yyyy-mm-dd)")
        if not re.match(height_pattern, height):
            raise ValueError(f"height {height} not valid (feet\'inches\")")
        if not re.match(weight_pattern, weight):
            raise ValueError(f"weight {weight} not valid (int)")
        if (not first_name) or (not last_name) or (not country) or (not position):
            raise ValueError(f"values missing")
        print(f"Player edit - data check")

        cursor.execute("SELECT id FROM team WHERE abbreviation = %s", (team_abbreviation,))
        team_id = cursor.fetchone()['id']
        if team_id is None:
            raise ValueError(f"Team {team_abbreviation} not found")
        cursor.execute(
            "update player set first_name = %s, last_name = %s, birthdate = %s, country = %s, height = %s, weight = %s, position = %s, team_id = %s where id = %s",
            (first_name, last_name, birthdate, country, height, weight, position, team_id, id)
        )
        connection.commit()
        print(f"Player edit - success")
    except Exception as e:
            connection.rollback()
            print(f"Failed to edit player: {e}")
            success = False
    finally:
        cursor.close()
    if success:
        return jsonify(response_success)
    return jsonify(response_failed), 500