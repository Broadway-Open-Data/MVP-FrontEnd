import os
import enum
import json
import datetime
from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import expression
from werkzeug.security import generate_password_hash, check_password_hash






db = SQLAlchemy()

class User(db.Model):
    """"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, nullable=False, default=lambda: int(str(int(uuid.uuid4()))[:7]), unique=True, index=True)
    date_instantiated = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)


    def __str__(self):
        return json.dumps({

            "id":self.id,
            "date_instantiated":self.date_instantiated.strftime("%Y-%m-%d %H:%M:%s"),

            # the basics:
            "email":self.email
        })

    """
    Set password stuff
    """
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
