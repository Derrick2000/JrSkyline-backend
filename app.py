#from resource import app
from src.config import app
from migration.blueprints.db_migration import migrate_team_info, test

if __name__ == '__main__':
    app.run(debug=True)
