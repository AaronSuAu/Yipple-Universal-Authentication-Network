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
    user = User(username, password)

    if username == "" or password == "":
        return 500

    rawData = komrade.read()
    if rawData == "":
        jsonData = json.loads(rawData)
        if username == jsonData['username']:
            return 400

    komrade.write(user.getJsonData())
    return 302

def validateUser(username, password):
    komrade = KomradeConfig("user")
    rawData = komrade.read()
    if rawData == "":
        pass

    jsonData = json.loads(rawData)
    if jsonData['username'] == username and jsonData['password'] == password:
        return 300
    else:
        return 403