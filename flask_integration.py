"""
Author: Andrew Rehmann
Date: 03/07/2024

This file contains the flask integration between the frontend and backend

"""

from flask import Flask, send_from_directory, jsonify, session, request
import DataInput
import AutoAssign
import login
import os

# Create an instance
app = Flask(__name__, static_folder="Frontend/")

# Create a secret key so that we can have session info
app.secret_key = os.urandom(24)

@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Origin"] = "*" # <- You can change "*" for a domain for example "http://localhost"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, PUT, DELETE"
    response.headers["Access-Control-Allow-Headers"] = "Accept, Content-Type, Content-Length, Accept-Encoding, X-CSRF-Token, Authorization"
    return response

# Endpoint for logging in as a user
@app.route('/user/login', methods=['POST'])
def flask_login_user():
    """
    Flask endpoint for logging in a user. Takes a POST request with a form
    attribute with a json/dict of keys 'user' and 'pass' corresponding to
    the username and password.

    Input:
        POST form request with 'user' and 'pass' keys
    Output:
        JSON reply with 'user_exists', 'pass_valid', and 'userid' parameters
        user_exists: False if the user doesn't exist, True if the user does exist.
        pass_valid: True if the password matches the user's, False otherwise.
        user_id: The user's ID on a successful login attempt, '' otherwise
    """
    reply = {
        'user_exists': False,
        'pass_valid': False
    }
    if request.method != 'POST':
        return jsonify(reply)

    username = request.form['user']
    password = request.form['pass']

    # Check if user exists
    if not login.verify_user_exists(username, DataInput.OCCUPANTS_FILEPATH):
        return jsonify(reply)
    
    reply['user_exists'] = True
    
    # Check if password is correct
    if login.log_in_user(username, password, DataInput.OCCUPANTS_FILEPATH):
        # Maybe not necessary to store user, since frontend handles it, but doesn't hurt
        session['user'] = username
        reply['user'] = username
        reply['pass_valid'] = True
        return jsonify(reply)
    else:
        return jsonify(reply)

# Endpoint for creating a user
@app.route('/user/create', methods=['POST'])
def flask_create_user():
    """
    Flask endpoint for creating a user. Takes a POST request with a form
    attribute with a json/dict of keys 'user' and 'pass' corresponding to
    the username and password.

    Input:
        POST form request with 'user' and 'pass' keys
    Output:
        JSON reply with 'success' parameter
        success: True if the user creation succeeded, False if it failed
    """
    reply = {
        'success': False
    }
    if request.method != 'POST':
        return jsonify(reply)
    username = request.form['user']
    password = request.form['pass']
    reply['success'] = login.create_user(username, password, DataInput.OCCUPANTS_FILEPATH)
    return jsonify(reply)

# Endpoint for listing users
@app.route('/user/serve', methods=['POST', 'GET'])
def flask_serve_users():
    """
    Flask endpoint for getting the users. Takes a GET request.

    Input:
        GET request
    Output:
        JSON reply with list of users and IDs
    """
    reply = []
    occupants_dict = DataInput.retrieve_occupants_names_and_uids(DataInput.OCCUPANTS_FILEPATH)
    reply = [{"name": username, "UserID": uid} for uid, username in occupants_dict.items()]
    return jsonify(reply)

# Endpoint for logging out as a user (unused)
@app.route('/user/logout')
def flask_logout_user():
    session["user"] = ''

# Endpoint for deleting a user
@app.route('/user/delete', methods=['POST'])
def flask_delete_user():
    """
    
    """
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        delete_success = login.delete_user(username, password, DataInput.OCCUPANTS_FILEPATH)
        if delete_success:
            session["user_id"] = None
        return jsonify({'success': delete_success})

# Endpoint for completing a chore
@app.route('/chore/complete', methods=['POST'])
def flask_complete_chore():
    """
    Flask endpoint for marking a chore as complete. Takes a POST request with a form
    attribute with a json/dict of keys 'Chore ID'

    Input:
        POST form request with 'Chore ID'
        Chore ID: The ID of the chore to be marked as complete
    Output:
        JSON reply with 'success' parameter
        success: True if the chore completion succeeded, False if it failed
    """
    reply = {'success': False}
    
    if request.method != 'POST':
        return jsonify(reply)
    
    chore_id = request.form['chore_id']
    DataInput.set_chore_complete(chore_id)
    AutoAssign.renew_repeating_chores()
    
    reply['success'] = True
    return jsonify(reply)

# Endpoint for creating a chore
@app.route('/chore/create', methods=['POST'])
def flask_create_chore():
    """
    Flask endpoint for creating a chore. Takes a POST request with a form
    attribute with a json/dict of keys 'Chore Name', 'Description'

    Input:
        POST form request with 'Chore ID'
        Chore ID: The ID of the chore to be marked as complete
    Output:
        JSON reply with 'success' parameter
        success: True if the chore completion succeeded, False if it failed
    """
    reply = {'success': False}
    if request.method != 'POST':
        return jsonify(reply)
    DataInput.new_chore_by_args(
        name = request.form['Chore Name'],
        desc = request.form['Description'],
        frequency = request.form['Frequency']
    )

    reply['success'] = True
    return jsonify(reply)

# Endpoint for serving (listing) chores
@app.route('/chore/serve', methods=['POST'])
def flask_serve_chores():
    """
    Flask endpoint for serving chores. Takes a POST request with a form
    attribute with a json/dict of keys 'user'

    Input:
        POST form request with 'user'
        user: The username of the provided user. Leave empty if fetching all chores
    Output:
        JSON reply with a list of the chores assigned to the user. Looks like:
        [
            {
                'Chore ID': *value*,
                'Chore Name': *value*,
                'Description': *value*,
                'Category': *value*,
                'Expected Duration': *value*,
                'Status': *value*,
                'Assignee ID': *value*,
                'Deadline Date': *value*,
                'Frequency': *value*,
                'Completion Date': *value*
            },
            ...
        ]
    """
    reply = []
    if request.method != 'POST':
        return jsonify(reply)
    
    username = request.form['user']
    
    if username:
        userid = DataInput.retrieve_occupant_uid_from_username(username, DataInput.OCCUPANTS_FILEPATH)
    else:
        userid = None
    
    chores = DataInput.get_chores_by_filters(assignee_id=userid, status=DataInput.CHORE_STATUS.ASSIGNED)
    reply = [{key: chore.to_csv_row()[key] for key in DataInput.CHORE_ATTRIBUTES} for chore in chores]
    return jsonify(reply)

# Endpoint for autoassigning chores
@app.route('/chore/assign', methods=['POST', 'GET'])
def flask_assign_chores():
    """
    Flask endpoint for autoassigning users. Takes a GET request.

    Input:
        GET request
    Output:
        None
    """
    if request.method == 'GET':
        reply = {}
        AutoAssign.assign_unassigned_chores()
        return jsonify(reply)


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# {fetch('http://localhost:5000/api/data')
#             .then(response => response.json())
#             .then(data => console.log(data))
#             }


if __name__ == '__main__':
    app.run(debug=True)