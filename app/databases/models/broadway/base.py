from databases import db
from databases.models import dbTable
from databases.models import broadway as broadway_models

# sqlalchemy stuff
from sqlalchemy.orm.collections import InstrumentedList

import datetime


def convert_to_tuple(value):
    """Helpful function"""

    # Null values
    if value==None:
        return (None,)

    # Single value
    if isinstance(value, (str,int, datetime.datetime)):
        return (value,)

    if isinstance(value, list):
        return tuple(value)

    if isinstance(value, tuple):
        return value




class BaseModel(dbTable):
    __table_args__ = {'schema':'broadway'}
    __bind_key__ = 'broadway'



    # Create highly specific function...
    def update_info_and_track(self, **kwargs):
        """Updates data and tracks edits"""

        self.track_change(**kwargs)

        if kwargs.get('test',False)==True:
            return

        self.update_info(**kwargs)




    # This works! Store values here...
    def track_change(self, **kwargs):

        # Get edit meta info
        edit_date = datetime.datetime.utcnow()
        user_edit_id = kwargs.get('edit_id', broadway_models.DataEdits().get_next_edit_id())


        # Who made the edit ? – This will have to be built as a wrapper I guess...
        edit_by = kwargs.get('edit_by', '__obd_application__')
        edit_comment = kwargs.get('edit_comment', 'Automated edit made through the open broadway data backend interface.')
        approved =  kwargs.get('approved', True)
        approved_by = kwargs.get('approved_by', '__obd_application__')
        approved_comment = kwargs.get('approved_comment', 'Automated edit made through the open broadway data backend interface.')


        # Get reference stuff
        table_name = self.__tablename__


        for key, value in kwargs.get('update_dict').items():

            # Get the value from the class...
            pre_value = getattr(self, key)

            # If the data type is a list of children
            if isinstance(pre_value, InstrumentedList):
                pre_value = [x.id for x in pre_value]


            # If no edit, then don't store
            # compare two lists...
            if (isinstance(pre_value, list) and set(pre_value)==set(value)) \
            or pre_value == value:
                if kwargs.get('debug',False)==True:
                    print("no edit needed")
                continue



            my_edit = broadway_models.DataEdits(
                edit_date=edit_date,
                user_edit_id=user_edit_id,
                edit_by=edit_by,
                edit_comment=edit_comment,
                edit_citation = kwargs.get('edit_citation'),
                approved=approved,
                approved_by=approved_by,
                approved_comment=approved_comment,
                table_name=table_name,
                value_primary_id=self.id,
                field = key,
                field_type = kwargs.get('field_type') if kwargs.get('field_type') else str(self.find_type(key)), # this is weird since the `.get` method valls the second value.....
            )


            if kwargs.get('debug',False)==True:
                print(my_edit.as_dict())


            # Don't save edit when testing.
            if kwargs.get('test',False)==False:
                my_edit.save_to_db()



            # ======== Save edit values ========

            all_values_pre = convert_to_tuple(pre_value)
            all_values_post = convert_to_tuple(value)


            def add_edit_values(values, pre_or_post:int):
                """Add values, pre or post..."""
                for val in values:
                    my_value = broadway_models.DataValues(value=val, pre_or_post=pre_or_post)

                    # Don't save edit value when testing.
                    if kwargs.get('test',False)==False:
                        my_value.save_to_db()

                    # Now save
                    if pre_or_post==0:
                        my_edit.data_values_pre.append(my_value)
                    else:
                        my_edit.data_values_post.append(my_value)


            # Now save them!
            add_edit_values(all_values_pre, 0)
            add_edit_values(all_values_post, 1)


            # Don't save edit when testing.
            if kwargs.get('test',False)==False:
                my_edit.save_to_db()











#
