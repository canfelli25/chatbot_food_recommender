import sys, pytest, random
from flask_script import Manager, Command
from flask_migrate import Migrate, MigrateCommand
from app import app
from foodmania.models import db

migrate = Migrate(app, db)
manager = Manager(app)

class Runserver(Command):
    "run the application"

    def run(self):
        app.run()

class Test(Command):
    "run unit test"

    def run(self):
        sys.exit(pytest.main([]))

class Seed(Command):
    "run to do data seeding"
    pass
    # def run(self):
    #     for i in range(50000):
    #         Drivers.add_driver({
    #             "latitude": 40+(i/1000000),
    #             "longitude": 130+(i/1000000),
    #             "accuracy": random.uniform(0.0, 1.0)
    #         })
    #     db.session.commit()

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Runserver())
manager.add_command('test', Test())
manager.add_command('seed', Seed())


if __name__ == '__main__':
    manager.run()