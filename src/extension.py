# # This file is used to avoid circular reference
from flask_sqlalchemy import SQLAlchemy
import pymysql
import pymysql.cursors
from src.config import DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_DB

db = SQLAlchemy()


def get_db_connection():
    return pymysql.connect(host=DATABASE_HOST,
                           user=DATABASE_USER,
                           password=DATABASE_PASSWORD,
                           database=DATABASE_DB,
                           cursorclass=pymysql.cursors.DictCursor)

