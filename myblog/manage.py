# encoding: utf-8
from app import app, db
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

manager = Manager(app)

# Using Migrate bind app and db
migration = Migrate(app, db)

# adding migration command to manager
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
