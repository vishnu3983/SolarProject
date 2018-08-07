<<<<<<< HEAD
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
=======
from flask import Flask
from flask_mongoengine import MongoEngine

#app initialization
app = Flask(__name__)

#configFiles
app.config.from_pyfile('config.py')

#mongoengine instance
db = MongoEngine(app)

from views import *



if __name__ == '__main__':
    app.run()
>>>>>>> de47050ad09df9b5ed8c8ffbb55a842d4c441b77
