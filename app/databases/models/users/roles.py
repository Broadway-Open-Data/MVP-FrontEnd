from databases import db, models
from . import BaseModel

from sqlalchemy.orm import validates
from flask_security import RoleMixin

import datetime


# ------------------------------------------------------------------------------

# Define models
roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('users.user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('users.role.id')),
        info={'bind_key': 'users'},
        schema='users'
    )



# ------------------------------------------------------------------------------


class Role(db.Model, RoleMixin, BaseModel):
    __tablename__ = "role"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    # Assert is lowercase
    @validates('name')
    def convert_lower(self, key, value):
        return value.lower()


    @classmethod
    def get_by_name(self, name):
        """Get the id, name, description of a role based on the role name"""
        return self.query.filter_by(name=name).first()

    # Show roles
    def __repr__(self):
        return f"{self.id}: {self.name}"
