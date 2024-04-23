from src.extension import db

import random
from datetime import datetime


class User(db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.now)


class Player(db.Model):
    __tablename__ = "Player"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.String(100))
    country = db.Column(db.String(100))
    height = db.Column(db.String(10))
    weight = db.Column(db.Integer)
    position = db.Column(db.String(20))
    team_id = db.Column(db.Integer)


class CommonPlayerInfo(db.Model):
    __tablename__ = "common_player_info"
    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    birthdate = db.Column(db.String(100))
    country = db.Column(db.String(100))
    height = db.Column(db.String(10))
    weight = db.Column(db.Integer)
    position = db.Column(db.String(20))
    team_name = db.Column(db.String(50))


class Game(db.Model):
    __tablename__ = "game"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    home_id = db.Column(db.Integer)
    away_id = db.Column(db.Integer)
    date = db.Column(db.String(50))
    home_score = db.Column(db.Integer)
    away_score = db.Column(db.Integer)


class CompositeTeam(db.Model):
    __tablename__ = "composite_team"
    game_id = db.Column(db.Integer, primary_key=True)
    team_name_home = db.Column(db.String(50))
    team_name_away = db.Column(db.String(50))


class CommonGame(db.Model):
    __tablename__ = "common_game"
    team_id_home = db.Column(db.Integer)
    team_id_away = db.Column(db.Integer)
    team_name_home = db.Column(db.String(50))
    team_name_away = db.Column(db.String(50))
    game_id = db.Column(db.Integer, primary_key=True)
    game_date = db.Column(db.String(50))
    pts_home = db.Column(db.Integer)
    pts_away = db.Column(db.Integer)




class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(1000))
    created_date = db.Column(db.DateTime, default=datetime.now)


class Team(db.Model):
    __tablename__ = "team"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    abbreviation = db.Column(db.String(45))
    nickname = db.Column(db.String(45))
    city = db.Column(db.String(45))
    year_founded = db.Column(db.Integer)


class TeamInfo(db.Model):
    __tablename__ = "team_info"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    full_name = db.Column(db.String(100), nullable=False)
    abbreviation = db.Column(db.String(10))
    nickname = db.Column(db.String(30))
    city = db.Column(db.String(30))
    year_founded = db.Column(db.Integer)

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "abbreviation": self.abbreviation,
            "nickname": self.nickname,
            "city": self.city,
            "year_founded": self.year_founded
        }



