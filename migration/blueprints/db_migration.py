#from resource.extension import db
from src.extension import db
from models import TeamInfo, Team, CommonPlayerInfo, Player, CommonGame, CompositeTeam, Game
from flask import Blueprint, jsonify
from migration.auto_gen import generate_news

bp = Blueprint("migration", __name__, url_prefix="/migration")


@bp.route("/player", methods=['GET', 'POST'])
def migrate_player_info():
    common_player_list = CommonPlayerInfo.query.all()
    for common_player in common_player_list:
        team_id = find_team_id_by_team_name(common_player.team_name)
        if team_id == -1:
            continue
        play = Player(first_name=common_player.first_name, last_name=common_player.last_name, birthdate=common_player.birthdate,
                      country=common_player.country, height=common_player.height, weight=common_player.weight, position=common_player.position,
                      team_id=team_id)
        db.session.add(play)
    db.session.commit()
    return None


@bp.route("/team", methods=['GET', 'POST'])
def migrate_team_info():
    team_info_list = TeamInfo.query.all()
    serialized_teams_info = []
    for team_info in team_info_list:
        serialized_teams_info.append(team_info.serialize())
    for team_info in team_info_list:
        application = Team(name=team_info.full_name, abbreviation=team_info.abbreviation, nickname=team_info.nickname, city=
                        team_info.city, year_founded=team_info.year_founded)
        db.session.add(application)
    db.session.commit()
    return jsonify(serialized_teams_info)


@bp.route("/news/add_auto_generated_news", methods=['POST'])
def add_auto_generated_news():
    for i in range(1505):
        news = generate_news()
        db.session.add(news)
    db.session.commit()
    response_object = {'status': 'success'}
    return jsonify(response_object)


@bp.route('/game', methods=['GET'])
def migrate_game():
    common_games = CommonGame.query.offset(63000).all()
    count = 0
    for cg in common_games:
        home_id = find_team_id_by_team_name(cg.team_name_home)
        away_id = find_team_id_by_team_name(cg.team_name_away)
        if home_id == -1 or away_id == -1:
            continue
        game = Game(home_id=home_id, away_id=away_id, date=cg.game_date, home_score=cg.pts_home, away_score=cg.pts_away)
        db.session.add(game)
        count += 1
    db.session.commit()
    response_object = {'status': 'success', 'count': count}
    return jsonify(response_object)


@bp.route('/composite_team', methods=['GET'])
def build_composite_team():
    games = Game.query.all()
    count = 0
    for game in games:
        home_name = find_team_name_by_team_id(game.home_id)
        away_name = find_team_name_by_team_id(game.away_id)
        if home_name == "" or away_name == "":
            continue
        ct = CompositeTeam(game_id=game.id, team_name_home=home_name, team_name_away=away_name)
        db.session.add(ct)
        count += 1
    db.session.commit()
    response_object = {'status': 'success', 'count': count}
    return jsonify(response_object)

@bp.route("/test", methods=['GET', 'POST'])
def test():
    print("test")
    response_object = {'status': 'success'}
    return jsonify(response_object)


def find_team_id_by_team_name(team_name):
    team_info = Team.query.all()
    for team in team_info:
        if team.name.lower() == team_name.lower():
            return team.id
    return -1


def find_team_name_by_team_id(team_id):
    team_info = Team.query.all()
    for team in team_info:
        if team_id == team.id:
            return team.name
    return ""
