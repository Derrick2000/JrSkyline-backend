from flask import Blueprint, jsonify, session, g, request
from src.extension import get_db_connection

bp_game = Blueprint("game", __name__, url_prefix="/game")


@bp_game.route("/getAllGame", methods=['GET'])
def get_all_game():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = ("select g.id, ht.name as home_name, wt.name as away_name, home_score, away_score, date from JrSkyline.game g "
               "join JrSkyline.team ht on g.home_id = ht.id join JrSkyline.team wt on g.away_id = wt.id order by date desc")
        cursor.execute(sql)
        game_list = cursor.fetchall()
    return jsonify(game_list)


@bp_game.route("/getGameById/<int:id>", methods=['GET'])
def get_game_by_id(id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "select * from game where id = %s"
        cursor.execute(sql, id)
        game = cursor.fetchone()
    return jsonify(game)


@bp_game.route("/deleteGameById/<int:id>", methods=['POST'])
def delete_game_by_id(id):
    response_object = {'status': 'success'}
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "delete from game where id = %s"
        cursor.execute(sql, id)
    connection.commit()
    return jsonify(response_object)


@bp_game.route("/updateGame/<int:id>", methods=['POST'])
def update_game(id):
    response_object = {'status': 'success'}
    connection = get_db_connection()
    away_score = request.json.get("away_score")
    home_score = request.json.get("home_score")
    away_id = request.json.get("away_id")
    home_id = request.json.get("home_id")
    date = request.json.get("date")

    with connection.cursor() as cursor:
        sql = "update game set away_score = %s, home_score = %s, date = %s, away_id = %s, home_id = %s where id = %s"
        cursor.execute(sql, (away_score, home_score, date, away_id, home_id, id))
    connection.commit()
    return jsonify(response_object)


@bp_game.route("/addGame", methods=['POST'])
def add_team():
    response_object = {'status': 'success'}
    connection = get_db_connection()
    away_score = request.json.get("away_score")
    home_score = request.json.get("home_score")
    away_id = request.json.get("away_id")
    home_id = request.json.get("home_id")
    date = request.json.get("date")

    with connection.cursor() as cursor:
        sql = "select id from game order by id desc limit 1"
        cursor.execute(sql)
        game_id = cursor.fetchone()['id'] + 1
        add_sql = "insert into game values(%s, %s, %s, %s, %s, %s)"
        cursor.execute(add_sql, (game_id, home_id, away_id, date, home_score, away_score))
    connection.commit()
    return jsonify(response_object)


@bp_game.route("/getGameById/<int:id>", methods=['GET'])
def get_team_by_id(id):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        sql = "select * from game where id = %s"
        cursor.execute(sql, id)
        team = cursor.fetchone()
    return jsonify(team)


@bp_game.route("/getHomeGamePlayed", methods=['GET'])
def get_home_game_played():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.callproc("GetGamePlayedHome")
        result = cursor.fetchall()
    return jsonify(result)


@bp_game.route("/getAwayGamePlayed", methods=['GET'])
def get_away_game_played():
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.callproc("GetGamePlayedAway")
        result = cursor.fetchall()
    return jsonify(result)


def create_game_stored_procedure():
    connection = get_db_connection()
    try:
        cursor = connection.cursor()
        cursor.execute("Use JrSkyline;")
        cursor.execute("DROP PROCEDURE IF EXISTS GetGamePlayedHome;")
        cursor.execute("DROP PROCEDURE IF EXISTS GetGamePlayedAway;")

        sp1 = """
            CREATE PROCEDURE GetGamePlayedHome()
            BEGIN
                IF (select count(*) from JrSkyline.team) = 30 THEN
                    SELECT home_name, COUNT(*) as num_occurrences
                    FROM (select g.id, t.name as home_name from JrSkyline.game g
                    join JrSkyline.team t on g.home_id = t.id) as temp
                    GROUP BY home_name;
                END IF;
            END;
        """

        sp2 = """
            CREATE PROCEDURE GetGamePlayedAway()
            BEGIN
                IF (select count(*) from JrSkyline.team) = 30 THEN
                    SELECT away_name, COUNT(*) as num_occurrences
                    FROM (select g.id, t.name as away_name from JrSkyline.game g
                    join JrSkyline.team t on g.away_id = t.id) as temp
                    GROUP BY away_name;
                END IF;
            END;
        """
        cursor.execute(sp1)
        cursor.execute(sp2)
        connection.commit()

    finally:
        connection.close()


create_game_stored_procedure()
