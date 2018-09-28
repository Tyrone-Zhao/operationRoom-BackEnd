from flask import Flask
from operationRoom.controllers.main import main_blueprint


def create_app(object_name):
    app = Flask(__name__)
    app.config.from_object(object_name)

    app.register_blueprint(main_blueprint)

    return app

if __name__ == '__main__':
    app = app = create_app('operationRoom.config.TestConfig')
    app.run()
