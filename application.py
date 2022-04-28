import datetime

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, \
    get_jwt_identity

application = Flask(__name__)
CORS(application)

application.config['JWT_SECRET_KEY'] = 'tserewara'
jwt = JWTManager(application)

db_users = [
    {
        'id': 1,
        'username': 'Alvaro',
        'password': 'pass123'
    },
    {
        'id': 2,
        'username': 'Tserewara',
        'password': 'pass123'
    }
]


def get_user(name, db):
    for user in db:
        if user['username'] == name:
            return user
    raise Exception('Wrong credentials')


def check_password(user, password):
    if user['password'] != password:
        raise Exception('Wrong credentials')
    return True

@application.route('/')
def home():
    return '<h1>Welcome from Elastic Beanstalk</h1>'


@application.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    try:

        user = get_user(username, db_users)
        if check_password(user, password):
            access_token = create_access_token(
                identity=user['id'],
                expires_delta=datetime.timedelta(minutes=30)
            )
            return jsonify({"token": access_token, "username": username})

    except Exception as e:
        return jsonify({'msg': str(e)})


@application.route('/secret')
@jwt_required()
def secret():
    current_user_id = get_jwt_identity()
    return jsonify({'msg': f'This route is secret {current_user_id}'}), 200



if __name__ == '__main__':
    application.run(host='0.0.0.0')
