"""
Author: Andrew Rehmann
Date: 03/07/2024

This file contains the flask integration between the frontend and backend

"""

from flask import Flask, send_from_directory, jsonify, session, request
import DataInput
from datetime import datetime, date
import login

# Create an instance
app = Flask(__name__, static_folder="Frontend/")
# Create a secret key so that we can have session info
app.secret_key = ''


# Endpoint for logging in as a user
@app.route('/user/login', methods=['POST'])
def flask_login_user():
    # If we get a post request, get the data from it
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        # login_success, userid = login.log_in_user(username, password, DataInput.OCCUPANTS_FILEPATH)
        if login.log_in_user(username, password, DataInput.OCCUPANTS_FILEPATH):
            session["user_id"] = 'userid'
            return jsonify({'successful': True, 'userid': 'userid'})
            # Set logged in user here? Have some class for that?
        else:
            return jsonify({'successful': False, 'userid': ''})

# Endpoint for logging out as a user
@app.route('user/logout')
def flask_logout_user():
    pass
    session["user_id"] = None
    # login.logout_user? un-set logged in user here.

@app.route('/user/delete', methods=['POST'])
def flask_delete_user():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['pass']
        delete_success = login.delete_user(username, password, DataInput.OCCUPANTS_FILEPATH)
        if delete_success:
            session["user_id"] = None
        return jsonify({'successful': delete_success})

@app.route('/chore/complete', methods=['POST'])
def flask_complete_chore():
    if request.method == 'POST':
        chore_id = request.form['chore_id']
        chore = DataInput.get_chore_by_id(chore_id)
        if chore:
            chore.completion_date = datetime.today()
            DataInput.update_chore(chore)

@app.route('/chore/create', methods=['POST'])
def flask_create_chore():
    if request.method == 'POST':
        DataInput.add_chore(DataInput.CHORES_FILEPATH)
        # Change this to take inputs and get them from post

@app.route('/chore/serve', methods=['POST'])
def flask_serve_chores():
    pass
    # Not sure if this should be using user info from backend or from frontend, 



@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# {fetch('http://localhost:5000/api/data')
#             .then(response => response.json())
#             .then(data => console.log(data))
#             }


if __name__ == '__main__':
    app.run(debug=True)