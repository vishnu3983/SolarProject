from app import app
from models import User
from flask import request, jsonify
import jwt
import random, time
from functools import wraps

def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'Authorization' in request.headers:
            auth = request.headers['Authorization']
            print(auth)
            if not check_auth(auth):
                return authenticate()
        else:
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def check_auth(accessToken):
    try:
        global payload, current_user
        payload = jwt.decode(accessToken, app.config['SECRET_KEY'])
        print(payload)
        current_user = User.objects.get(email=payload['email'])
    except jwt.ExpiredSignatureError:
        return False
    return True

                    #AUTHENTICATION
@app.route('/login', methods=['POST'])
def loginMethod():
    content=request.get_json(force=True)
    refreshKey = random.getrandbits(32)
    if User.objects(email=content['email'], password=content['password']):
        user=User.objects.get(email=content['email'], password=content['password'])
    else:
        return jsonify({'result': 'fail', 'message': 'invalid email or password'})

    if user.refreshSecret:
        refreshKey=user.refreshSecret
    else:
        refreshKey = random.getrandbits(32)
        user.refreshSecret = refreshKey
        user.save()

    refreshToken = jwt.encode({'refreshSecret': refreshKey, 'email': user.email}, app.config['SECRET_KEY'],
                              algorithm='HS256')
    return jsonify({'result': 'success', 'message': str(refreshToken)})

#Access Token Endpoint
@app.route('/getAccessToken', methods=['POST'])
def getAccessToken():
    content = request.get_json(force=True)
    print(content)
    refreshToken = content['refreshToken']
    payload = jwt.decode(refreshToken, app.config['SECRET_KEY'])
    print(payload['refreshSecret'])
    user = User.objects.get(refreshSecret=payload['refreshSecret'])

    if not user:
        print("fail")
        return jsonify({"message": "fail"})
    else:
        print(user)
        print(user.email)
        secs = int(time.time())
        accessToken = jwt.encode({'email': user.email, 'exp': secs + 360}, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'result': 'success', 'message': str(accessToken)})

                    #USER MANAGEMENT
#create user endpoint
@requires_auth
@app.route('/users/create', methods=['POST'])
def createUserMethod():
    content = request.get_json()
    if User.objects(email=content['email']):
        return jsonify({'result': 'fail', 'message': 'User already exists'})
    else:
        user = User(email=content['email'], password=content['password'], role=content['role'])
        user.save()
        return jsonify({'result': 'success', 'message': 'User created'})

#delete user endpoint
@requires_auth
@app.route('/users/delete', methods=['POST'])
def deleteUserMethod():
    content = request.get_json()
    if not User.objects(email=content['email']):
        return jsonify({'result': 'fail', 'message': 'User does not exist'})
    else:
        user = User.objects(email=content['email'])
        user.delete()
        return jsonify({'result': 'success', 'message': 'User deleted'})
