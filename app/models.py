from app import db
from config import BOARDS 

boardtabs = {}

for k, v in BOARDS.items():
    exec("""class Post_%s(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        body = db.Column(db.String(1800))
        timestamp = db.Column(db.DateTime)
        trip = db.Column(db.String(10))
        ip = db.Column(db.String(39))
        thread = db.Column(db.Integer)
        bump = db.Column(db.Integer, default="0")
        sage = db.Column(db.Integer)
        subject = db.Column(db.String(100))
        banned = db.Column(db.Integer)
        locked = db.Column(db.Integer)
        sticky = db.Column(db.Integer)""" % k)
    exec("boardtabs[\"%s\"] = Post_%s" % (k, k))

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    trip = db.Column(db.String(10))
    ip = db.Column(db.String(39))
    subject = db.Column(db.String())

class Ban_global(db.Model):
    __tablename__ = 'BAN_GLOBAL' 
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String)
    reason = db.Column(db.String)
    length_until = db.Column(db.DateTime)
