from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()

# Command
# python manage.py db init      - create migration folder (only run one time)
# python manage.py db migrate   - run migration (run every time models change)
# python manage.py db upgrade   - upgrade (run every time models change)

