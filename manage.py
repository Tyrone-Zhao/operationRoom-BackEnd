import os

from flask_script import Manager, Server
from operationRoom import create_app

# default to dev config
env = os.environ.get('operationRoom_ENV', 'dev')
app = create_app('operationRoom.config.%sConfig' % env.capitalize())


manager = Manager(app)
manager.add_command("server", Server())


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
