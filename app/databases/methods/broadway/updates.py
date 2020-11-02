from databases.models.broadway import Person, GenderIdentity, RacialIdentity, race_table, DataEdits
from databases.models import db
import datetime as dt

from flask_login import current_user

def update_people_data(params):
    """
    Update a person's data.

    Does not return anything.
    """

    # Rules
    assert (isinstance(params, dict))
    assert(isinstance(params['person_id'], int))
    my_person = Person.get_by_id(params['person_id'])


    edit_comment = params.get(
        "edit_comment",
        f"Edit made by '{current_user.email}' through the open broadway data `contribute` interface."
        )


    # Default, start off with an edit id
    edit_id = DataEdits().get_next_edit_id()

    # ==========================================================================

    # 1. Update racial identities
    if params.get('racial_identity'):

        # this works for gender identity and racial identity
        update_person_identities(
            person_id=1,
            attr='racial_identity',
            children_names=params.get('racial_identity'),
            track_changes=True,
            # meta stuff
            edit_id=edit_id,
            edit_by=current_user.email,
            edit_comment=edit_comment,
            approved_comment=f"Edit made by '{current_user.email}' through the open broadway data `contribute` interface.",
        )

    # ==========================================================================

    # 2. Date of birth
    if params.get('date_of_birth'):
        date_of_birth = dt.datetime.strptime(params.get('date_of_birth'), "%m/%d/%Y")

        my_person.update_info_and_track(
            update_dict={'date_of_birth':date_of_birth},
            # meta stuff
            edit_id=edit_id,
            edit_by=current_user.email,
            edit_comment=edit_comment,
            approved_comment=f"Edit made by '{current_user.email}' through the open broadway data `contribute` interface.",
            debug=False
            )


    # ==========================================================================



    # Gender identity
    if params.get('gender_identity'):

        # reload the person?
        my_person = Person.get_by_id(params['person_id'])

        my_gender = GenderIdentity.get_by_name(params['gender_identity'])

        # If the gender identity doesn't exist, create it...
        if not my_gender:
            my_gender = GenderIdentity(name=params['gender_identity'], description=f"Created by '{current_user.email}' through the OBD app.")
            my_gender.save_to_db()

        # now set the person's gender identity
        my_person.update_info_and_track(
            update_dict={'gender_identity_id':my_gender.id},
            # meta stuff
            edit_id=edit_id,
            edit_by=current_user.email,
            edit_comment=edit_comment,
            approved_comment=f"Edit made by '{current_user.email}' through the open broadway data `contribute` interface.",
            debug=False
            )


    # ==========================================================================


    # if params.get('racial_identities'):
    #
    #     # reload the person?
    #     my_person = Person.get_by_id(params['person_id'])
    #
    #
    #     # convert to a set
    #     racial_identities = set()
    #     for x in params.get('racial_identities').split(','):
    #         x = x.strip()
    #         if x:
    #             racial_identities.add(x)
    #
    #     # ----------------------------------------------------------------------
    #
    #     previous_ids = [x.id for x in my_person.racial_identity]
    #
    #     ALL_racial_identities = []
    #
    #     # Step 1: convert from string to a racial identity
    #     for x in racial_identities:
    #         my_racial_identity = RacialIdentity.get_by_name(x)
    #
    #         # If the racial identity doesn't exist, create it...
    #         if not my_racial_identity:
    #             my_racial_identity = RacialIdentity(name=x, description=f"Created by '{current_user.email}' through the OBD app.")
    #             my_racial_identity.save_to_db()
    #
    #         # save to list
    #         ALL_racial_identities.append(my_racial_identity)
    #
    #     # -  -  -  -  -  -  -  -  -  -  -  -  -
    #
    #     # Step 2: remove racial identities
    #     for x in my_person.racial_identity:
    #         if x not in ALL_racial_identities:
    #             my_person.racial_identity.remove(x)
    #
    #     # -  -  -  -  -  -  -  -  -  -  -  -  -
    #
    #     # Step 3: add them
    #     for x in ALL_racial_identities:
    #         # now set the person's racial identity
    #         if x not in my_person.racial_identity:
    #             my_person.racial_identity.append(x)
    #
    #     # -  -  -  -  -  -  -  -  -  -  -  -  -
    #
    #     # updated ids
    #     updated_ids = [x.id for x in my_person.racial_identity]
    #
    #     # Only continue if changes are made
    #     if previous_ids==updated_ids:
    #         return
    #
    #
    #     # ----------------------------------------------------------------------
    #
    #     # Get edit meta info
    #     user_edit_id = db.session.query(DataEdits.user_edit_id).order_by(-DataEdits.user_edit_id.asc()).first()
    #
    #     # Unpack the tuple to a result
    #     if user_edit_id: user_edit_id = user_edit_id[0] + 1
    #     else: user_edit_id = 1
    #
    #     # Comments
    #     approved_comment =f"Edit made by '{current_user.email}' through the open broadway data `contribute` interface.",
    #
    #
    #     my_edit = DataEdits(
    #         edit_date=dt.datetime.utcnow(),
    #         user_edit_id=user_edit_id,
    #         edit_by=current_user.email,
    #         edit_comment=edit_comment,
    #         approved=True,
    #         approved_by=current_user.email,
    #         approved_comment=approved_comment,
    #         table_name=Person.__tablename__,
    #         value_primary_id=my_person.id,
    #         field = 'racial_identities (relationship)',
    #         field_type = 'LIST (INTEGERS)',
    #         value_pre = ', '.join(map(str, previous_ids)),
    #         value_post = ', '.join(map(str, updated_ids)),
    #         edit_citation=params.get('edit_citation')
    #     )
    #
    #     # Save the edit message
    #     my_edit.save_to_db()
    #
    #     # Save the changes
    #     my_person.save_to_db()

        # -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -



def update_person_identities(person_id:int, attr:str, children_names:list, track_changes=True, **kwargs):
    """
    Updates a person for the given criteria

    Params:
        person_id: (int) the id of the person
        attr: (str) the attribute which you'd like to update (ex: racial_identity)
        children_names: (list, str) a list of (str) names of the children to be updated (ex: ['white','british'])
        track_changes: (bool) track changes and store in data_edits table? (default True)
    """

    my_person = Person.get_by_id(person_id)


    # ----------------------------------------------------------------------
    # 1. Track changes without updating

    curr_children = getattr(my_person, attr)
    field_type = 'RELATIONSHIP (LIST CHILD.IDS)' # this is the max str length (40 chars)

    # You must pass a list of racial identity ids
    # Conver a list of names to ids with the following:
    if attr=='racial_identity':
        new_children = [RacialIdentity.get_by_name(x) for x in children_names]
    elif attr=='gender_identity':
        new_children = [GenderIdentity.get_by_name(x) for x in children_names]
    else:
        raise NameError(f'{attr} not recognized')


    new_children_ids = [x.id for x in new_children]

    # Finally, track the changes
    my_person.track_change(
        update_dict={attr: new_children_ids},
        field_type = 'RELATIONSHIP (LIST CHILD.IDS)',
        debug=False,
        test=False,
        **kwargs
        )


    # ----------------------------------------------------------------------
    # Update values

    # remove current ids first:
    for child in getattr(my_person, attr):
        if child not in new_children:
            getattr(my_person, attr).remove(child)

    # Now add ids
    for child in new_children:
        if child not in getattr(my_person, attr):
            getattr(my_person, attr).append(child)

    # Now save...
    my_person.save_to_db()










    # if params.get('gender_identity'):
    #     my_gender = GenderIdentity.get_by_name(params['gender_identity'].lower())
