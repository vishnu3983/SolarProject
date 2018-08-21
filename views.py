from app import app
from models import *
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
    content = request.get_json(force=True)
    refreshKey = random.getrandbits(32)
    if User.objects(email=content['email'], hashedPassword=content['password']):
        user = User.objects.get(email=content['email'], hashedPassword=content['password'])
    else:
        return jsonify({'result': 'fail', 'message': 'invalid email or password'})

    if user.refreshSecret:
        refreshKey = user.refreshSecret
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
        user = User(email=content['email'], hashedPassword=content['password'], role=content['role'])
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


@app.route('/getZoneControllerInfo/<string:zoneID>', methods=['GET'])
def getZoneControllerInfo(zoneID):
    print(zoneID)
    zone = Zone.objects.get(zoneID=zoneID)
    row_data = []
    row_ids = []
    row_id = StaticRow.objects(zoneID=zoneID)          #getting row ids with zoneID as StaticRow objects
    for row in range(zone.rows):
        row_ids.append(row_id[row].id)                  #getting objectID of each row using StaticRow objects
        row_data.append(StaticRow.objects.get(id=row_ids[row]))         #StaticRow data of zoneID as a list

    data = {'ZoneData': zone, 'RowData': row_data}

    return jsonify({'result': 'success', 'message': data})

@app.route('/getStaticData', methods=['GET'])
def getStaticData():
    data = []
    zone_ids = []
    zone_data = []
    zone_id = Zone.objects()
    for zone in range(Zone.objects.count()):
        zone_ids.append(zone_id[zone].id)                 #getting zone ids
        zone_data.append(Zone.objects.get(id=zone_ids[zone]))    #zone data
        row_data = []
        row_ids = []
        zoneID = zone_data[zone]['zoneID']
        row_id = StaticRow.objects(zoneID=zoneID)          #getting row ids using zoneID, as StaticRow objects
        for row in range(zone_data[zone]['rows']):
            row_ids.append(row_id[row].id)                  #getting objectID of each row using StaticRow objects
            row_data.append(StaticRow.objects.get(id=row_ids[row]))         #StaticRow data of zoneID as a list

        data.append({'ZoneData': zone_data[zone], 'RowData': row_data})      #static zone data + all of its row's static data

    return jsonify({'result': 'success', 'message': data})                   #returning all static data as [{'zoneData':zone1, 'rowData':{row1, row2 ...}}, {'zoneData':zone2, 'rowData':{row1,row2, ...}, ...]

@app.route('/getHistoricalData/<timeStamp>', methods=['GET'])
def getHistoricalDataMethod(timeStamp):
    rowDataReq = []
    rowData_objectIDs = []
    rowData_objects = DynamicRow.objects()
    for data in range(DynamicRow.objects.count()):
        rowData_objectIDs.append(rowData_objects[data].id)
        rowData = DynamicRow.objects.get(id=rowData_objectIDs[data])
        if int(rowData.timeStamp) >= int(timeStamp):
            rowDataReq.append(rowData)

    return jsonify({'result': 'success', 'message': rowDataReq})