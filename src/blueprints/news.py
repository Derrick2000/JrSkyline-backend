from flask import Blueprint, jsonify, session, g, request
from src.models import User
from werkzeug.security import check_password_hash, generate_password_hash
# from src.extension import db
from datetime import datetime
from src.extension import get_db_connection

bpN = Blueprint("news", __name__, url_prefix="/news")

@bpN.route('/get_news', methods=['GET'])
def get_news():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM news"
            cursor.execute(sql)
            news_data = cursor.fetchall()
            #print(news_data)
        return jsonify(news_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@bpN.route('/edit_news', methods=['POST'])
def edit_news():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
           data = request.json
           news_id = data.get("id")
           title = data.get('title')
           print(title)
           content = data.get('content')
           sql = "UPDATE news SET title=%s, content=%s WHERE id=%s"
           cursor.execute(sql, (title, content, news_id))
           connection.commit()
           session.clear()
        return jsonify({'message': 'News item updated successfully'})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@bpN.route('/add_news', methods=['POST'])
def add_news():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Extract title and content from the request
            data = request.json
            title = data.get('title')
            content = data.get('content')
            # Insert the new news item into the database
            today_date = datetime.today().strftime("%B %d, %Y")
            #print(today_date)
            sql = "INSERT INTO news (title, content,created_date) VALUES (%s, %s,%s)"
            cursor.execute(sql, (title, content, today_date))
            connection.commit()
            new_news_id = cursor.lastrowid
        return jsonify({'id': new_news_id, 'message': 'News item added successfully'})
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

@bpN.route('/delete_news', methods=['POST'])
def delete_news():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            data = request.json
            news_id = data.get('id')
            # Delete the news item from the database
            sql = "DELETE FROM news WHERE id = %s"
            cursor.execute(sql, (news_id,))
            connection.commit()
        return jsonify({'message': 'News item deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()