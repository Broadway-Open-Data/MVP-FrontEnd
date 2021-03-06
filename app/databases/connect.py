import sys
import os
import json
import sys
import datetime
import uuid


# Correct the path
sys.path.insert(1, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Internal stuff
from create_db import db
from databases.models.broadway import Person, Show, DataEdits, RacialIdentity, GenderIdentity
from databases.methods.broadway import update_person_identities
from utils.get_db_uri import get_db_uri


# Flask Stuff
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Data stuff
import pandas as pd



# Define args
import argparse

parser = argparse.ArgumentParser(description='describe the name of the operation you want to do -- using the function name / class method.')
parser.add_argument('function_name', nargs='*', help='name of the class method you want to run')



# ------------------------------------------------------------------------------


class ConnectApp():

    def __init__(self, **kwargs):

        # Instantiate a blank app
        self.app = Flask(__name__)
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app.config['SQLALCHEMY_BINDS'] = {
            'users': get_db_uri("users"),
            'broadway': get_db_uri("broadway"),
        }

        # instantiate the db
        self.app.app_context().push()
        db.init_app(app=self.app)
        db.create_all()

    # ------------------------------------------------------------------------------

    # Create some methods
    def nick(self):
        my_person = Person.query.filter_by(f_name='nick', l_name='spangler').first()

        my_show = Show.query.filter(Show.title.ilike('%%book of mormon%%')).first()

        if my_show in my_person.shows:
            print(f'{my_person.f_name.title()} has been in {my_show.title}')

        # Use a class method
        res = my_person.is_in_this_show(my_show.id)

        # Another approach
        # res = my_show.person_in_this_show(my_person.id)
        # print(res)




    def query_all_users(self):
        """Get all existing show ids"""

        query = """
        SELECT
            id
        FROM
            users.user
        ;
        """
        result = db.get_engine(bind='users').execute(query)
        all_ids = [int(x[0]) for x in result]
        return all_ids



    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def test_single_change(self):

        # Alt:
        my_person = Person.get_by_id(18174)

        # print(my_person.__dict__)
        curr_g_id = my_person.gender_identity_id

        new_g_id = 1 if curr_g_id==2 else 2

        # Update value
        my_person.update_info_and_track(update_dict={'gender_identity_id':new_g_id}, debug=True, test=False)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def test_multi_change(self):
        """Try changing multiple things"""

        # Alt:
        my_person = Person.get_by_id(18174)
        print("pre:", my_person.racial_identity)

        # ----------------------------------------------------------------------
        # Just track the change, don't update...

        curr_racial_ids = getattr(my_person, 'racial_identity') # maybe it's in here....

        if len(curr_racial_ids)==2:
            new_racial_identity = ['white']
        else:
            new_racial_identity = ['white','british']


        update_person_identities(18174, 'racial_identity', new_racial_identity, track_changes=True)

        print("post:", my_person.racial_identity)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    def update_gender(self, person_id=18174):
        """Try changing multiple things"""

        # Alt:
        my_person = Person.get_by_id(person_id)
        curr_gender_ids = my_person.gender_identity # will be single value:

        print("pre:", my_person.gender_identity)

        if not curr_gender_ids:
            return

        # otherwise
        curr_gender_ids = [x.name for x in curr_gender_ids]

        if 'non binary' not in curr_gender_ids:
            curr_gender_ids.append('non binary')
        else:
            curr_gender_ids.remove('non binary')

        # let's give it a go...
        update_person_identities(person_id, 'gender_identity', curr_gender_ids, track_changes=True)

        print("post:", my_person.gender_identity)

    # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -

    # Done with this function...






if __name__ =='__main__':

    args = parser.parse_args()

    db_app = ConnectApp()

    if 'nick' in args.function_name:
        db_app.nick()

    if 'query_all_users' in args.function_name:
        all_user_ids = db_app.query_all_users()
        print(all_user_ids)

    # Test the functionality of the update stuff
    if 'test_single_change' in args.function_name:
        db_app.test_single_change()

    # Test the functionality of the update stuff
    if 'test_multi_change' in args.function_name:
        db_app.test_multi_change()

    if 'update_gender' in args.function_name:
        db_app.update_gender()





#
