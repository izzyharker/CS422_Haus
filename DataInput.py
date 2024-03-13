"""
Author: Carter Young, Alex JPS, Connie Williamson, Andrew Rehmann
Date: 02/24/24

This module provides getter and setter functions with which the frontend and the automatic chore assignment
modules can interact with the Household Data Storage database (the CSV files in the csvs/ directory).
"""

# python libraries
import json
import csv
import uuid
from datetime import datetime, date, timedelta

# enhanced typing
from typing import Union
from enum import Enum

# Constant definitions

# Attributes which every chore must have, coincides with names in line 1 of chores.csv
CHORE_ATTRIBUTES = ['Chore ID',
                    'Chore Name',
                    'Description',
                    'Category',
                    'Expected Duration',
                    'Status',
                    'Assignee ID',
                    'Deadline Date',
                    'Frequency',
                    'Completion Date']


# Symbolic constants for chore statuses
class CHORE_STATUS(Enum):
    UNASSIGNED = "unassigned"  # chore is newly created
    ASSIGNED = "assigned"  # chore has been assigned to a user
    COMPLETED = "completed"  # chore has been completed by that user
    RENEWED = "renewed"  # (of repeating chores) chore is renewed and should not be renewed again


# Chore CSV file location
CHORES_FILEPATH = 'csvs/chores.csv'

# Occupants CSV file location
OCCUPANTS_FILEPATH = 'csvs/occupants.csv'

# Chore rankings file location
CHORE_RANKINGS_FILEPATH = 'csvs/chore_rankings.csv'

# date format to be used in all CSVs
DATE_FORMAT = '%Y-%m-%d'

"""
Chore Class
"""


class Chore:
    """
    Class representing a chore.
    This class simplifies working with chores and their attributes on the server-side.
    Please note: Chore objects must be converted to JSON when interacting with frontent.
    """
    name: str
    id: str
    description: str
    category: str
    expected_duration: int
    status: CHORE_STATUS
    assignee_id: Union[str, None]
    deadline_date: Union[date, None]
    frequency: int
    completion_date: Union[date, None]

    def __init__(self, csv_chore_row: dict):
        """
        Constructor to create a Chore object based on a dict from a chore CSV row.
        This is not a means to create a new chore, but rather to have an object-oriented
        representation of a chore to be communicated between modules in the backend.
        That is why an ID is expected to arleady exist,
        """
        self.name = csv_chore_row["Chore Name"]
        self.id = csv_chore_row["Chore ID"]
        self.description = csv_chore_row["Description"]
        self.category = csv_chore_row["Category"]
        self.expected_duration = int(csv_chore_row["Expected Duration"])
        self.status = CHORE_STATUS(csv_chore_row["Status"])
        self.assignee_id = csv_chore_row["Assignee ID"] \
            if csv_chore_row["Assignee ID"] else None
        self.deadline_date = datetime.strptime(csv_chore_row["Deadline Date"], DATE_FORMAT).date() \
            if csv_chore_row["Deadline Date"] else None
        self.frequency = int(csv_chore_row["Frequency"]) if csv_chore_row["Frequency"] else 0
        self.completion_date = datetime.strptime(csv_chore_row["Completion Date"], DATE_FORMAT).date() \
            if csv_chore_row["Completion Date"] else None

    def __str__(self):
        """Return a string representation of every aspect of the chore"""
        return f"""
        Name: {self.name}
        ID: {self.id}
        Description: {self.description}
        Category: {self.category}
        Expected Duration: {self.expected_duration}
        Status: {self.status.value}
        Assignee ID: {self.assignee_id}
        Deadline Date: {self.deadline_date}
        Frequency: {self.frequency}
        Completion Date: {self.completion_date}
        """

    def to_csv_row(self) -> dict[str, str]:
        """
        Return a dict representing the chore's attribute as a CSV row for the database.
        """
        return {
            "Chore ID": self.id,
            "Chore Name": self.name,
            "Description": self.description,
            "Category": self.category,
            "Expected Duration": str(self.expected_duration),
            "Status": self.status.value,
            "Assignee ID": self.assignee_id,
            "Deadline Date": self.deadline_date.strftime(DATE_FORMAT) if self.deadline_date else "",
            "Frequency": str(self.frequency),
            "Completion Date": self.completion_date.strftime(DATE_FORMAT) if self.completion_date else ""
        }


"""
Setter Functions
"""


def add_occupant_name(filename: str, occupant_uid: str, occupant_username: str, occupant_password: str) -> bool:
    """Adds a username and password to the occupants CSV file. Also generates a UID for the new user.
    Note: does not verify if this name already exists. That functionality is covered in the login.py module
    as this module is strictly concerned with passing data."""
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([occupant_uid, occupant_username, occupant_password])
    # print(f"Added {occupant_username} with UID {occupant_uid} and password {occupant_password} to house.")
    return True


def new_chore_by_object(chore: Chore) -> None:
    """
    Given a Chore object, add a new entry to the CSV database.
    The Chore object may or may not have an ID already.
    If not, a new ID will be generated for it.
    """
    # if chore does not have an id, generate a unique one
    if not chore.id:
        chore.id = generate_uid()

    # read existing chores to check that it does not already exist (based on id)
    with open(CHORES_FILEPATH, 'r') as file:
        reader = csv.DictReader(file)
        lines = list(reader)
    for line in lines:
        if line["Chore ID"] == chore.id:
            raise ValueError("Chore ID already exists in database")

    # add new chore to the list and write back to the file
    lines.append(chore.to_csv_row())
    with open(CHORES_FILEPATH, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=CHORE_ATTRIBUTES)
        writer.writeheader()
        writer.writerows(lines)


def new_chore_by_args(name: str,
                      desc: str, 
                      id: Union[str, None] = None,
                      category: str = "", 
                      expected_duration: int = 10,
                      status: Union[CHORE_STATUS, None] = CHORE_STATUS.UNASSIGNED, 
                      assignee_id: Union[str, None] = None,
                      frequency: int = 0,
                      deadline_date: Union[date, None] = None,
                      completion_date: Union[date, None] = None) -> None:
    """
    Adds a new chore to the CSV database with the given attributes.
    """
    # If chore doesn't have an id, generate a unique one
    if not id:
        id = generate_uid()

    # If chore doesn't have a deadline, set it to today + frequency
    if not deadline_date:
        deadline_date = date.today() + timedelta(days=frequency)
    deadline_date_text = deadline_date.strftime(DATE_FORMAT)

    # read existing chores to check that it does not already exist (based on id)
    with open(CHORES_FILEPATH, 'r') as file:
        reader = csv.DictReader(file)
        lines = list(reader)
    for line in lines:
        if line["Chore ID"] == id:
            raise ValueError("Chore ID already exists in database")
    csv_row = {
            'Chore ID': id,
            'Chore Name': name,
            'Description': desc,
            'Category': category,
            'Expected Duration': expected_duration,
            'Status': status,
            'Assignee ID': assignee_id,
            'Deadline Date': deadline_date_text,
            'Frequency': frequency,
            'Completion Date': completion_date
    }
    new_chore = Chore(csv_row)
    new_chore_by_object(new_chore)


def update_chore_by_object(chore: Chore) -> None:
    """
    Given a Chore object, update the CSV database entry to match object's attributes.
    If the chore does not exist (no ID or ID not in CSV database), throw error.
    """
    # find the chore in the CSV database by id
    with open(CHORES_FILEPATH, 'r') as file:
        reader = csv.DictReader(file)
        lines = list(reader)
    chore_found = False
    for i in range(len(lines)):
        if lines[i]["Chore ID"] == chore.id:
            chore_found = True
            # update the line with the new chore attributes
            lines[i] = chore.to_csv_row()
            break
    if not chore_found:
        raise ValueError("Chore ID not found in database")

    # write everything back to the file
    with open(CHORES_FILEPATH, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=CHORE_ATTRIBUTES)
        writer.writeheader()
        writer.writerows(lines)


def set_chore_complete(chore_id: str) -> None:
    """
    Change the status of the chore with the given id to completed.
    This also sets the "Completion Date" attribute to the current date.
    Updates the chores.csv database file accordingly.
    """
    # find the chore in the CSV database by id
    with open(CHORES_FILEPATH, 'r') as file:
        reader = csv.DictReader(file)
        lines = list(reader)
    chore_found = False
    for i in range(len(lines)):
        if lines[i]["Chore ID"] == chore_id:
            chore_found = True
            # make sure the chore is assigned and has an assignee ID
            if lines[i]["Status"] != CHORE_STATUS.ASSIGNED.value:
                raise ValueError("Chore must first be assigned to be completed")
            if not lines[i]["Assignee ID"]:
                raise ValueError("Chore must first be assigned to someone to be completed")
            # update the line with the new chore attributes
            lines[i]["Status"] = CHORE_STATUS.COMPLETED.value
            lines[i]["Completion Date"] = date.today().strftime(DATE_FORMAT)
            break
    if not chore_found:
        raise ValueError("Chore ID not found in database")
    # write everything back to the file
    with open(CHORES_FILEPATH, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=CHORE_ATTRIBUTES)
        writer.writeheader()
        writer.writerows(lines)
        

def remove_user(username: str, occupant_filepath: str) -> None:
    """
    Remove a user from the occupants CSV. Does not verify if the user exists beforehand.
    This function does not verify that the deletion is authorized, as that should be left to the login module.
    """
    # open the occupants CSV and extract all the info currently there
    # don't extract the data we're removing
    current_user_info = []
    with open(occupant_filepath, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            if row[1] != username:  # usernames are stored in the second column. Copy all usernames except the one we're deleting
                current_user_info.append(row)

    # write all extracted data back in
    with open(occupant_filepath, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(current_user_info)


"""
Getter Functions
"""


def get_username_list(filename: str) -> list[str]:
    """
    Returns the list of usernames stored in the occupants CSV file
    """
    current_usernames = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            current_usernames.append(row[1])

    # trim Username header
    current_usernames = current_usernames[1:]

    return current_usernames


def get_password(filename: str, username: str) -> str:
    """
    Returns the password for a given username from the occupants CSV file
    """
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[1] == username:
                return row[2]

    # username isn't valid, so return nothing


def retrieve_occupants_names_and_uids(OCCUPANTS_FILEPATH: str) -> dict[str, str]:
    """
    Return a dictionary object mapping occupant IDs to their names.
    """
    occupants = {}
    with open(OCCUPANTS_FILEPATH, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header

        for row in reader:
            occupants[row[0]] = row[1]
    return occupants
  
  
def retrieve_occupant_uid_from_username(username: str, OCCUPANTS_FILEPATH: str) -> str:
    """
    Returns the first instance of a uid matching the input username
    """
    with open(OCCUPANTS_FILEPATH, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header

        for row in reader:
            if row[1] == username:
                return row[0]


def get_chore_by_id(id: str) -> Chore:
    """
    Return a Chore object from database by id
    """
    # first find the chore in the CSV database by id
    found_csv_row = None
    file = open(CHORES_FILEPATH, 'r')
    reader = csv.DictReader(file)
    for row in reader:
        if row['Chore ID'] == id:
            found_csv_row = row
            break
    if not found_csv_row:
        return None
    # create a chore object from the row
    chore = Chore(found_csv_row)
    file.close()
    return chore


def get_chores_by_filters(assignee_id: str = None,
                          status: CHORE_STATUS = None,
                          min_deadline_date: date = None,
                          max_deadline_date: date = None,
                          repeating_only: bool = False
                          ) -> list[Chore]:
    """
    Return a list of Chore objects matching the given filters.
    The list will be empty if none of the chores in the database match.
    """
    matching_chores = []
    with open(CHORES_FILEPATH, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            chore = Chore(row)
            if repeating_only and (not chore.frequency or chore.frequency == 0):
                continue
            if status and chore.status != status:
                continue
            if assignee_id and chore.assignee_id != assignee_id:
                continue
            if min_deadline_date and (not chore.deadline_date or chore.deadline_date < min_deadline_date):
                continue
            if max_deadline_date and (not chore.deadline_date or chore.deadline_date > max_deadline_date):
                continue
            matching_chores.append(Chore(row))
    return matching_chores


def get_user_ids() -> list[str]:
    """
    Return a list of all user IDs in the database.
    """
    file = open('csvs/occupants.csv', 'r')
    reader = csv.DictReader(file)
    user_ids = []
    for row in reader:
        user_ids.append(row["Occupant UID"])
    file.close()
    return user_ids


"""
Other/Helper Functions
"""


def generate_uid() -> str:
    """
    This function generates a unique key, which can be used to
    identify a chore or a Haus occupant.
    """
    return str(uuid.uuid4())


def ensure_csv_headers(filename: str, headers: list[str]) -> None:
    """
    Ensures that the CSV file at filename contains the headers specified in the headers list.
    """
    try:
        with open(filename, 'r+', newline='') as file:
            # Try to read the first row and check if the headers match
            reader = csv.reader(file)
            existing_headers = next(reader, None)

            if not existing_headers or existing_headers != headers:
                print(f"Adding missing headers to {filename}")
                # File is empty or headers do not match, adding headers
                # Move to the start of the file to overwrite or prepend headers
                file.seek(0, 0)
                writer = csv.writer(file)
                writer.writerow(headers)

                # If the file was not empty but headers were incorrect, we need to preserve existing data
                if existing_headers:
                    # Move writer cursor to the end of the file
                    file.seek(0, 2)
                    # Write what was read as the first row back into the file, assuming it's actual data
                    writer.writerow(existing_headers)

    except FileNotFoundError:
        # File does not exist, creating new file with headers
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)


if __name__ == "__main__":
    raise Exception("This module is not meant to be run on its own. Please import it into another module.")
