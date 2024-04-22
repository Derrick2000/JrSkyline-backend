#DB
HOSTNAME = "127.0.0.1"
PORT = 3306
USERNAME = "root"
PASSWORD = "Aa54646498.."
DATABASE = "JrSkyline"
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)

# DB_URI = 'mysql+mysqlconnector://root:test1234@104.198.130.194:PORT/DATABASE'
SQLALCHEMY_DATABASE_URI = DB_URI


SECRET_KEY = 'JrSkyline_key'
SESSION_TYPE = 'filesystem'
