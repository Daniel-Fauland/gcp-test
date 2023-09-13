from . import db 
from sqlalchemy.sql import func

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime(timezone=True), default=func.now())
    name = db.Column(db.String(255), unique=True)
