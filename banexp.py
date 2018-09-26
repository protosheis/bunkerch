from app import app, db, models
from app.models import Ban_global, Ban_b 
from config import BANNED
import datetime

timey = datetime.datetime.utcnow()
timey = timey.replace(microsecond=0)

bansg = db.session.query(Ban_global).all()
for l in bansg:
    gsnab = db.session.qeury(Ban_global).filter_by(l.id).first()
    if gsnab.length_until >= timey:
        db.session.delete(gsnab)
    else:
        pass

bansb = db.session.query(Ban_b).all()
for l in bansb:
    bsnab = db.session.qeury(Ban_b).filter_by(l.id).first()
    if bsnab.length_until >= timey:
        db.session.delete(bsnab)
    else:
        pass
