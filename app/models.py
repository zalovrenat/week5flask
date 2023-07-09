from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    # __tablename__ = 'user'
    user_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(45),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String,nullable=False)
    date_created = db.Column(db.DateTime,nullable=False,default=datetime.utcnow())

    def __init__(self,username,email,password):
        self.username = username
        self.email = email
        self.password = password
    
    def get_id(self):
        try:
            return str(self.user_id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None