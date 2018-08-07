from flask import Flask
from flask_mongoengine import MongoEngine
from flask_mqtt import Mqtt

#app initialization
app = Flask(__name__)

#configFiles
app.config.from_pyfile('config.py')

#Mqtt instance
#mqtt = Mqtt(app)

#mongoengine instance
db = MongoEngine(app)

from views import *



if __name__ == '__main__':
    app.run()
