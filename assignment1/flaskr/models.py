import os
import json
import bcrypt
import uuid


class KomradeConfig:
    def __init__(self, name):
        self.config_file = os.path.join(os.path.dirname(__file__), "../" + name + ".json")

        if not os.path.exists(self.config_file):
            open(self.config_file, "w").write("{}")

    def read(self):
        return json.loads(open(self.config_file, "r").read())

    def write(self, data):
        with open(self.config_file, 'w') as fh:
            fh.write(json.dumps(data))


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def getJsonData(self):
        jsonData = "{\"username\":\""+self.username+"\", \"password\":\""+self.password+"\"}"
        return jsonData

def registerUser(username, password):
    komrade = KomradeConfig("user")

    if not username or not password:
        return 500

    users = komrade.read()

    if users != "":
        if "data" in users:
            for key in users['data']:
                temp = json.loads(key)
                if temp["username"] == username:
                    return 400
        else:
            users['data'] = []
    #users[username] = bcrypt.hashpw(password, bcrypt.gensalt())
    password = password.encode("utf-8")
    hashPass = bcrypt.hashpw(password, bcrypt.gensalt())
    userId = str(uuid.uuid4())
    userData = {'username':username, 'password':hashPass, 'userId':userId}
    userData = json.dumps(userData)

    users['data'].append(userData)
    komrade.write(users)
    return 302

def validateUser(username, password):
    komrade = KomradeConfig("user")
    password = password.encode("utf-8")
    users = komrade.read()
    if not users:
        return 403
    for key in users['data']:
        temp = json.loads(key)
        temp['password'] = temp['password'].encode("utf-8")
        if temp['username'] == username and bcrypt.checkpw(password, temp['password']):
            return temp['userId']
    return 403