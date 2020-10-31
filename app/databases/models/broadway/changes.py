from databases import db, models
from . import BaseModel
from sqlalchemy.sql import expression
from sqlalchemy.sql.expression import and_
import datetime

# ------------------------------------------------------------------------------



class DataEditsValuesLink(db.Model, BaseModel):
    """A 'link table' for data_edits and data_values"""
    __tablename__ = "data_edits_values_link"

    data_edits_id = db.Column(db.Integer,db.ForeignKey('broadway.data_edits.id'), primary_key=True)
    value_id = db.Column(db.Integer,db.ForeignKey('broadway.data_values.id'), primary_key=True)

    # Alternatively, use this value here to then decide if values are pre or post.... (and drop the extra table...)
    pre_or_post = db.Column(db.Boolean, nullable=False, comment='`0` represents `pre`, `1` represents `post`')

    def __repr__(self):
        return f"id: {self.data_edits_values_id}; value: {self.value_id}; {'PRE' if self.pre_or_post==0 else 'POST'}"



class DataValues(db.Model, BaseModel):
    """Stores values as related by the data edits table"""
    __tablename__ = "data_values"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    value = db.Column(db.String(300), nullable=True, unique=False)

    def __repr__(self):
        return f"id: {self.id}; value: {self.value}"





class DataEdits(db.Model, BaseModel):
    """"""
    __tablename__ = "data_edits"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # can be used to groupby...
    user_edit_id = db.Column(db.Integer, nullable=False, unique=False, primary_key=True)
    edit_date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    # edit details
    table_name = db.Column(db.String(80), nullable=False, unique=False)
    value_primary_id = db.Column(db.Integer, nullable=False, unique=False) # This is the row referred to in the edit..

    field = db.Column(db.String(40), nullable=False, unique=False)
    field_type = db.Column(db.String(40), default="VARCHAR(40)", nullable=False, unique=False)


    value_pre = db.Column(db.String(300), nullable=True, unique=False)
    value_post = db.Column(db.String(300), nullable=False, unique=False)

    # Who made the edit ?
    edit_by = db.Column(db.String(40), nullable=False, unique=False)
    edit_comment = db.Column(db.String(300), nullable=True, unique=False)
    edit_citation = db.Column(db.String(200), nullable=True, unique=False)

    # who approved the edit?
    approved = db.Column(db.Boolean, server_default=expression.false(), nullable=False)
    approved_by = db.Column(db.String(40), nullable=False, unique=False)
    approved_comment = db.Column(db.String(300), nullable=True, unique=False)


    # Not including values here just yet...
    data_values_pre = db.relationship("DataValues",
                            secondary="data_edits_values_link",
                            primaryjoin="data_values.id==data_edits_values_link.value_id",
                            secondaryjoin="and_( \
                                data_edits.id==data_edits_values_link.data_edits_id, \
                                data_edits_values_link.pre_or_post==0 \
                                )",
                            backref=db.backref("data_edits", lazy='joined'),
                            lazy='dynamic'
                            )

    data_values_post = db.relationship("DataValues",
                            secondary="data_edits_values_link",
                            primaryjoin="data_values.id==data_edits_values_link.value_id",
                            secondaryjoin="and_( \
                                data_edits.id==data_edits_values_link.data_edits_id, \
                                data_edits_values_link.pre_or_post==1 \
                                )",
                            backref=db.backref("data_edits", lazy='joined'),
                            lazy='dynamic'
                            )

    # data_values = db.relationship(DataValues, secondary='broadway.data_edits_values_link', backref=db.backref('broadway.data_edits_values', lazy='dynamic'), passive_deletes=True)










    # the basics
