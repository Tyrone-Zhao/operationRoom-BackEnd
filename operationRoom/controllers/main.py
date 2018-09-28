from flask import Blueprint, jsonify
from operationRoom.models import DB, db_config
import random
import json


main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)


@main_blueprint.route('/')
def index():
    return "hello world"


@main_blueprint.route('/json', methods=['GET'])
def return_json():
    if random.randint(0, 5) >= 2:
        return_dict = {
            "data": True,
            "code": 0,
            "msg": "string"
        }
    else:
        return_dict = {
            "data": False,
            "code": 0,
            "msg": "string"
        }

    return jsonify(return_dict)


@main_blueprint.route('/database', methods=['GET'])
def database_test():
    db = DB()
    result = db.select_sql("select * from name;")[0]
    db.close()
    return json.dumps(result, ensure_ascii=False)


