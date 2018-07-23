from app import db

class User(db.Document):
    email = db.StringField(unique=True)
    password = db.StringField()
    refreshSecret = db.LongField()
    role = db.StringField()