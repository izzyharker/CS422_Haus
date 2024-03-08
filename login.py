"""
Author: Connie Williamson
Date: 03/3/2024

This file represents the log in module.

Inputs:
- Username and password from user

Outputs:
- Status of log-in attempt (either successful or unsuccessful)
"""
import DataInput

def create_user(username, password, occupant_filepath):
    """Verifies that the user doesn't already exist, then adds to the haus. 
    If user is successfully added, returns True.
    If user already exists, returns False.
    """
    # if this is the first name to be added, ensure that the headers are correct
    DataInput.ensure_csv_headers(occupant_filepath, ['Occupant UID', 'Username', 'Password'])
    occupant_uid = DataInput.generate_uid()

    # check that someone with this username doesn't already exist
    if verify_user_exists(username, occupant_filepath): 
        print("Username already exists!")
        return False
    
    # actually write the info into the CSV file
    return DataInput.add_occupant_name(occupant_filepath, occupant_uid, username, password)


def delete_user(username, password, occupant_filepath):
    """Verifies that a user exists, then removes from the haus"""
    pass

def log_in_user(username, password, occupant_filepath):
    """Verifies that a username and password are valid and logs in the user attached to those credentials.
    Returns True on a successful log-in attempt, false otherwise
    """
    # TODO: create a user class so we can keep track of who is logged in
    # this log in function should set that user class to change on a successful attempt
    # first verify if the username is a valid username
    if not verify_user_exists(username, occupant_filepath):
        print("Username not valid!")
        return False
    
    # username is valid
    # check if password given is correct for the username
    expected_password = DataInput.get_password(occupant_filepath, username)
    if expected_password != password:
        print("Password not valid!")
        return False
    
    # TODO: interact with frontend and chore system here to actually log this person in
    return True
    

def verify_user_exists(username, occupant_filepath):
    """Returns True if a username belongs to a user in the haus, False otherwise"""
    current_usernames = DataInput.get_username_list(occupant_filepath)
    return username in current_usernames