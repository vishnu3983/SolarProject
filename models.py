from app import db

class Weather(db.Document):
    anaemometer = db.StringField()
    pyranometer = db.StringField()
    site = db.IntField()
    timeStamp = db.IntField()

class Position(db.EmbeddedDocument):
    lat = db.FloatField()
    lng = db.FloatField()
    alt = db.FloatField()
    azimuthDeviation = db.StringField()
    pitch = db.FloatField()
    rowWidth = db.IntField()

class Zone(db.Document):
    siteName = db.StringField()
    siteID = db.StringField()
    rows = db.IntField()
    zoneID = db.StringField()
    firmwareVersion = db.StringField()
    position = db.EmbeddedDocumentField(Position)
    meta = {'collection': 'Zone'}

class User(db.Document):
    name = db.StringField()
    email = db.StringField(unique=True)
    hashedPassword = db.StringField()
    refreshSecret = db.LongField()
    role = db.StringField()
    meta = {'collection': 'User'}

class Stow(db.EmbeddedDocument):
    snowStow = db.FloatField()
    windStow = db.FloatField()
    nightStow = db.FloatField()
    cleanStow = db.FloatField()

class Limits(db.EmbeddedDocument):
    east = db.FloatField()
    west = db.FloatField()

class StaticRow(db.Document):
    siteName = db.StringField()
    siteID = db.StringField()
    zoneID = db.StringField()
    rowID = db.StringField()
    firmwareVersion = db.StringField()
    boardSerialNo = db.StringField()
    stow = db.EmbeddedDocumentField(Stow)
    limits = db.EmbeddedDocumentField(Limits)
    position = db.EmbeddedDocumentField(Position)
    meta = {'collection': 'StaticRow'}

class Motor(db.EmbeddedDocument):
    trackingResolution = db.IntField()
    status = db.StringField()
    cumulativeHours = db.IntField()
    current = db.FloatField()
    inclinometerAngle = db.FloatField()

class Battery(db.EmbeddedDocument):
    voltage = db.FloatField()
    current = db.FloatField()
    soc = db.FloatField()
    temp = db.FloatField()

class Pv(db.EmbeddedDocument):
    voltage = db.FloatField()
    current = db.FloatField()

class Tracking(db.EmbeddedDocument):
    targetAngle = db.FloatField()
    sunAngle = db.FloatField()
    inclinometerAngle = db.FloatField()

class Misc(db.EmbeddedDocument):
    RTC = db.LongField()
    snowDepth = db.FloatField()
    windSpeed = db.FloatField()
    ambientTemp = db.FloatField()
    boardTemp = db.FloatField()

class Led(db.EmbeddedDocument):
    power = db.StringField()
    comm = db.StringField()
    motor = db.StringField()
    mode = db.StringField()
    master = db.StringField()

class Events(db.EmbeddedDocument):
    time = db.LongField()
    desc = db.StringField()

class DataReceived(db.EmbeddedDocument):
    motorUpdate = db.EmbeddedDocumentField(Motor)
    battery = db.EmbeddedDocumentField(Battery)
    pv = db.EmbeddedDocumentField(Pv)
    tracking = db.EmbeddedDocumentField(Tracking)
    misc = db.EmbeddedDocumentField(Misc)
    led = db.EmbeddedDocumentField(Led)
    events = db.EmbeddedDocumentListField(Events)

class DynamicRow(db.Document):
    timeStamp = db.LongField()
    motor = db.EmbeddedDocumentField(Motor)
    dataRecieved = db.EmbeddedDocumentField(DataReceived)
    meta = {'collection': 'DynamicRow'}

