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
