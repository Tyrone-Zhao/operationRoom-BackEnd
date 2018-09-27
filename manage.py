import os

from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand

from deep_understand_flask import create_app
from deep_understand_flask.models import db, User, Post, Tag, Comment

# default to dev config
env = os.environ.get('deep_understand_flask_ENV', 'dev')
app = create_app('deep_understand_flask.config.%sConfig' % env.capitalize())

migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("server", Server())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Post=Post,
        Tag=Tag,
        Comment=Comment
    )


@manager.command
def test():
    """Run the unit tests"""
    import unittest
    tests = unittest.TestLoader().discover('test')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == "__main__":
    manager.run()
