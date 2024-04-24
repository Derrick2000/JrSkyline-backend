from flask import Blueprint, jsonify, session, g, request
from src.extension import get_db_connection


bp_team = Blueprint("team", __name__, url_prefix="/team")


@bp_team.route("/getAll", methods=['GET'])
def get_all_team():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "select * from team"
        cursor.execute(sql)
        team_list = cursor.fetchall()
    return jsonify(team_list)


@bp_team.route("/getTeamById/<int:id>", methods=['GET'])
def get_team_by_id(id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "select * from team where id = %s"
        cursor.execute(sql, id)
        team = cursor.fetchone()
    return jsonify(team)


@bp_team.route("/deleteTeamById/<int:id>", methods=['POST'])
def delete_team_by_id(id):
    response_object = {'status': 'success'}
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "delete from team where id = %s"
        cursor.execute(sql, id)
    connection.commit()
    return jsonify(response_object)


@bp_team.route("/updateTeam/<int:id>", methods=['POST'])
def update_team(id):
    response_object = {'status': 'success'}
    connection = get_db_connection()
    name = request.json.get("name")
    abbreviation = request.json.get("abbreviation")
    nickname = request.json.get("nickname")
    city = request.json.get("city")
    year_founded = request.json.get("year_founded")

    with connection.cursor() as cursor:
        sql = "update team set name = %s, abbreviation = %s, nickname = %s, city = %s, year_founded = %s where id = %s"
        cursor.execute(sql, (name, abbreviation, nickname, city, year_founded, id))
    connection.commit()
    return jsonify(response_object)


@bp_team.route("/addTeam/", methods=['POST'])
def add_team():
    response_object = {'status': 'success'}
    connection = get_db_connection()
    name = request.json.get("name")
    abbreviation = request.json.get("abbreviation")
    nickname = request.json.get("nickname")
    city = request.json.get("city")
    year_founded = request.json.get("year_founded")

    with connection.cursor() as cursor:
        sql = "select id from team order by id desc limit 1"
        cursor.execute(sql)
        team_id = cursor.fetchone()['id'] + 1
        add_sql = "insert into team values(%s, %s, %s, %s, %s, %s)"
        cursor.execute(add_sql, (team_id, name, abbreviation, nickname, city, year_founded))
    connection.commit()
    return jsonify(response_object)



