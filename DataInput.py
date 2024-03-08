"""
Author: Carter Young, Alex JPS, Connie Williamson
Date: 02/24/24

This file represents the data input module. It also enables all data input to be stored in the appropriate file type.
Inputs:
- House, Roommate, and Chore definitions from user

Outputs:
- JSON files for Houses, Roommates, and Chores
"""

import json
import csv
import uuid
from datetime import datetime, date
from enum import Enum
from typing import Union

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
                    'Completion Date']

# Symbolic constants for chore statuses
class CHORE_STATUS(Enum):
    UNASSIGNED = "unassigned"
    ASSIGNED = "assigned"
    COMPLETED = "completed"

# Chore CSV file location
CHORES_FILEPATH = 'csvs/chores.csv'

# Occupants CSV file location
OCCUPANTS_FILEPATH = 'csvs/occupants.csv'

# Chore rankings file location
CHORE_RANKINGS_FILEPATH = 'csvs/chore_rankings.csv'

# date format to be used in all CSVs
DATE_FORMAT = '%Y-%m-%d'

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
    completion_date: Union[date, None]

    def __init__(self, csv_chore_row: dict):
        """
        Constructor to create a Chore object based on a dict from a chore CSV row
        """
        self.name = csv_chore_row["Chore Name"]
        self.id = csv_chore_row["Chore ID"]
        self.description = csv_chore_row["Description"]
        self.category = csv_chore_row["Category"]
        self.expected_duration = int(csv_chore_row["Expected Duration"])
        self.status = CHORE_STATUS(csv_chore_row["Status"])
        self.assignee_id = csv_chore_row["Assignee ID"]
        self.deadline_date = datetime.strptime(csv_chore_row["Deadline Date"], DATE_FORMAT).date() \
            if csv_chore_row["Deadline Date"] else None
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
        Completion Date: {self.completion_date}
        """


def convert_csv_to_json(csv_filename, json_filename):
    """ Converts CSV to JSON for Flask/React """
    # Init data to empty
    data = []

    # Open CSV
    with open(csv_filename, 'r', newline='') as csv_file:
        # Create reader
        csv_reader = csv.DictReader(csv_file)
        # Loop over CSV rows
        for row in csv_reader:
            # Append data
            data.append(row)

    # Open JSON to write
    with open(json_filename, 'w', newline='') as json_file:
        # Write and pp
        json.dump(data, json_file, indent=4)


def generate_uid():
    """ This function generates a unique key for a Haus. """
    return str(uuid.uuid4())


def ensure_csv_headers(filename, headers):
    """ This function ensures all CSVs have the appropriate and specified headers. """
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


def append_to_csv(filename, data):
    """ Appends user input to csv """
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)


def get_haus_info():
    """ Ask user for haus information
    Inputs:
    - Haus name
    - Haus type
    - Num Occupants
    """
    haus_name = input("Enter Haus name: ")
    while True:
        haus_type = input("Enter Haus type (condo, apt, or house): ").lower()
        if haus_type in ['condo', 'apt', 'house']:
            break
        else:
            print("Invalid Haus type. Please enter 'condo', 'apt', or 'house'.")

    # Ensure num_people is assigned a value before it's used or returned.
    while True:
        num_people = input("Enter the number of people living there: ")
        if num_people in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']:
            break
        else:
            print("Invalid Quantity. Please enter an int.")

    return haus_name, haus_type, num_people

def get_username_list(filename):
    """Returns the list of usernames stored in the occupants CSV file"""
    current_usernames = []
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            current_usernames.append(row[1])
        
    # trim Username header        
    current_usernames = current_usernames[1:]

    return current_usernames

def get_password(filename, username):
    """Returns the password for a given username from the occupants CSV file"""
    with open(filename, mode='r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
             if row[1] == username:
                return row[2]
             
    # username isn't valid, so return nothing
             
def add_occupant_name(filename, occupant_uid, occupant_username, occupant_password):
    """Adds a username and password to the occupants CSV file. Also generates a UID for the new user.
    Note: does not verify if this name already exists. That functionality is covered in the login.py module
    as this module is strictly concerned with passing data."""
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([occupant_uid, occupant_username, occupant_password])
    # print(f"Added {occupant_username} with UID {occupant_uid} and password {occupant_password} to house.")
    return True


def verify_uid_and_get_occupants(filename, uid):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == uid:  # Assuming UID is always in the first column
                return int(row[3]), True
    return 0, False


def save_occupant_names(filename, occupant_uid, occupant_name):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([occupant_uid, occupant_name])


def initialize_chores(CHORES_FILEPATH):
    default_chores = [
        (
            generate_uid(), "Dishes", "Wash and dry the dishes", "Kitchen", "15", CHORE_STATUS.UNASSIGNED.value, None,
            None,
            None),
        (
            generate_uid(), "Dishes", "Wash and dry the dishes", "Kitchen", "15", CHORE_STATUS.UNASSIGNED.value, None,
            None,
            None),
        (generate_uid(), "Laundry", "Wash, dry, and fold clothes", "General", "20", CHORE_STATUS.UNASSIGNED.value, None,
         None, None),
        (generate_uid(), "Vacuum", "Vacuum all carpets and rugs", "General", "30", CHORE_STATUS.UNASSIGNED.value, None,
         None, None),
        (generate_uid(), "Dusting", "Dust all surfaces", "General", "20", CHORE_STATUS.UNASSIGNED.value, None, None,
         None),
        (generate_uid(), "Trash", "Take out the trash and recycling", "General", "5", CHORE_STATUS.UNASSIGNED.value,
         None, None, None),
        (generate_uid(), "Bathroom", "Clean the toilets and showers", "Bathroom", "35", CHORE_STATUS.UNASSIGNED.value,
         None, None, None),
        (generate_uid(), "Sweeping", "Sweep floors", "Floors", "20", CHORE_STATUS.UNASSIGNED.value, None, None, None),
        (generate_uid(), "Mopping", "Mop floors", "Floors", "20", CHORE_STATUS.UNASSIGNED.value, None, None, None)
    ]
    try:
        with open(CHORES_FILEPATH, 'r') as file:
            pass
    except FileNotFoundError:
        with open(CHORES_FILEPATH, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CHORE_ATTRIBUTES)
            for chore in default_chores:
                writer.writerow(chore)


def rank_chores(OCCUPANTS_FILEPATH, CHORES_FILEPATH, CHORE_RANKINGS_FILEPATH):
    """ This function allows users to rank chores """
    occupants = retrieve_occupants_names_and_uids(OCCUPANTS_FILEPATH)

    if not occupants:
        print("No occupants found.")
        return

    print("\nOccupants:")
    for occupant_uid, occupant_name in occupants.items():
        print(f"{occupant_name} (UID: {occupant_uid})")

    occupant_uid = input("Enter the UID of the occupant ranking chores: ").strip()
    if occupant_uid not in occupants:
        print("Occupant UID not found.")
        return

    print("\nChores:")
    chores = list_chores(CHORES_FILEPATH)
    rankings = []
    for chore_id, chore_name, _, _, _, _, _, _, _ in chores:
        valid_rank = False
        while not valid_rank:
            rank = input(f"Rank for {chore_name} (0, 1, or 2): ").strip()
            if rank in ['0', '1', '2']:
                valid_rank = True
                rankings.append((occupant_uid, chore_id, rank))
            else:
                print("Invalid rank. Please enter 0, 1, or 2.")

    save_chore_rankings(CHORE_RANKINGS_FILEPATH
, rankings)


def retrieve_occupants_names_and_uids(OCCUPANTS_FILEPATH):
    occupants = {}
    with open(OCCUPANTS_FILEPATH, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header

        for row in reader:
            occupants[row[0]] = row[1]
        """
        # Removing option to add house (deprecated)
        for row in reader:
            if row[0] == house_uid:
                # Assuming the format is: House UID, Occupant UID, Occupant Name
                occupants[row[1]] = row[2]
        """
    return occupants


def add_or_remove_chores(CHORES_FILEPATH):
    """Allows users to add or remove chores from the list."""
    action = input("Do you want to add or remove a chore? (add/remove): ").lower()
    if action == 'add':
        add_chore(CHORES_FILEPATH)
    elif action == 'remove':
        remove_chore(CHORES_FILEPATH)
    else:
        print("Invalid action. Please enter 'add' or 'remove'.")


def add_chore(CHORES_FILEPATH):
    """Adds a new chore to the chores list."""
    chore_name = input("Enter the name of the chore: ")
    description = input("Enter the chore description: ")
    category = input("Enter the chore category: ")
    expected_duration = input("Enter the estimated time to complete the chore (in minutes): ")
    chore_id = generate_uid()  # Using UUID for unique chore identifiers

    with open(CHORES_FILEPATH, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            [chore_id, chore_name, description, category, expected_duration, CHORE_STATUS.UNASSIGNED.value, None, None,
             None])

    print(f"Chore '{chore_name}' added successfully.")


def remove_chore(CHORES_FILEPATH):
    """Removes a chore from the chores list."""
    chore_name = input("Enter the name of the chore to remove: ")
    temp_chores = []
    chore_found = False

    with open(CHORES_FILEPATH, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Capture headers
        for row in reader:
            if row[1] != chore_name:  # Assuming chore name is in the second column
                temp_chores.append(row)
            else:
                chore_found = True

    if chore_found:
        with open(CHORES_FILEPATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write the headers back
            writer.writerows(temp_chores)  # Write the remaining chores
        print(f"Chore '{chore_name}' removed successfully.")
    else:
        print("Chore not found.")


def list_chores(CHORES_FILEPATH):
    chores = []
    with open(CHORES_FILEPATH, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            chores.append(row)
    return chores


def save_chore_rankings(CHORE_RANKINGS_FILEPATH, rankings):
    with open(CHORE_RANKINGS_FILEPATH
, mode='a', newline='') as file:
        writer = csv.writer(file)
        for ranking in rankings:
            writer.writerow(ranking)

# getter functions, for user by other modules importing this one

def get_chore_by_id(id: str):
    """Return a Chore object from database by id"""
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
    return chore

def get_chores_by_filters(assignee_id: str = None,
               status: CHORE_STATUS = None,
               min_deadline_date: date = None,
               max_deadline_date : date = None) -> list[Chore]:
    """
    Return a list of Chore objects matching the given filters.
    The list will be empty if none of the chores in the database match.
    """
    matching_chores = []
    file = open(CHORES_FILEPATH, 'r')
    reader = csv.DictReader(file)
    for row in reader:
        chore = Chore(row)
        if status and chore.status != status:
            continue
        if assignee_id and chore.assignee_id != assignee_id:
            continue
        if min_deadline_date and (not chore.deadline_date or chore.deadline_date < min_deadline_date):
            continue
        if max_deadline_date and (not chore.deadline_date or chore.deadline_date > max_deadline_date):
            continue
        matching_chores.append(Chore(row))
    file.close()
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

def update_chore(chore: Chore) -> None:
    """
    Given a Chore object, update the CSV database entry to match object's attributes.
    If the chore does not exist (no ID or ID not in CSV database), throw error.
    """
    # find the chore in the CSV database by id
    file = open(CHORES_FILEPATH, 'r')
    reader = csv.DictReader(file)
    lines = list(reader)
    for line in lines:
        if line["Chore ID"] == chore.id:
            # update the line with the new chore attributes
            line["Chore Name"] = chore.name
            line["Description"] = chore.description
            line["Category"] = chore.category
            line["Expected Duration"] = chore.expected_duration
            line["Status"] = chore.status.value
            line["Assignee ID"] = chore.assignee_id
            line["Deadline Date"] = chore.deadline_date.strftime(DATE_FORMAT) \
                if chore.deadline_date else ""
            line["Completion Date"] = chore.completion_date.strftime(DATE_FORMAT) \
                if chore.completion_date else ""
            break
    file.close()
    # write everything back to the file
    file = open(CHORES_FILEPATH, 'w', newline='')
    writer = csv.DictWriter(file, fieldnames=CHORE_ATTRIBUTES)
    writer.writeheader()
    writer.writerows(lines)
    file.close()


# FIXME We are not using category preferences for now, either remove or reinstate later in development
# def get_user_category_preferences(user_id: str) -> list[tuple[str, int]]:
#     """
#     Return a list of (category, preference) tuples for the given user_id.
#     The preferences can be 0 (negative), 1 (neutral), or 2 (positive).
#     """
#     file = open('csvs/chore_rankings.csv', 'r')
#     reader = csv.DictReader(file)
#     preferences = []
#     for row in reader:
#         if row["Occupant UID"] == user_id:
#             # TODO implement rankings based on category and not chore ID, and change "ranking" -> "preference"
#             preferences.append((row["Chore UID"], row["Rank"]))
#     file.close()
#     return preferences

# TODO remove this once frontend works
def main():
    # Initialize files
    # ensure_csv_headers(dwelling_file, ['House Name', 'House Type', 'Num Occupants'])
    ensure_csv_headers(OCCUPANTS_FILEPATH, ['Occupant UID', 'Username', 'Password'])
    ensure_csv_headers(CHORE_RANKINGS_FILEPATH
, ['Occupant UID', 'Chore UID', 'Rank'])
    initialize_chores(CHORES_FILEPATH)
    ensure_csv_headers(CHORES_FILEPATH, CHORE_ATTRIBUTES)

    # Convert 'hauses.csv' to 'hauses.json'
    # convert_csv_to_json('csvs/hauses.csv', 'jsons/hauses.json')
    # Convert 'occupants.csv' to 'occupants.json'
    convert_csv_to_json('csvs/occupants.csv', 'jsons/occupants.json')
    # Convert 'chores.csv' to 'chores.json'
    convert_csv_to_json('csvs/chores.csv', 'jsons/chores.json')
    # Convert 'chore_rankings.csv' to 'chore_rankings.json'
    convert_csv_to_json('csvs/chore_rankings.csv', 'jsons/chore_rankings.json')

    # Main menu loop
    # Removed option to add a house
    while True:
        print("\nMenu:")
        # print("1. Add a new Haus")
        # print("1. Add occupants to an existing Haus")
        print("2. Rank chores for a Haus")
        print("3. Add or remove a chore")
        print("4. Exit")
        choice = input("Select an option (1/2/3/4): ")

        # Removed option to add a house
        """
        if choice == '1':
            name, dwelling_type, num_people = get_haus_info()
            unique_key = generate_uid()
            append_to_csv(dwelling_file, [unique_key, name, dwelling_type, num_people])
            print(f"New Haus added with unique key: {unique_key}")
            break
        """
        # if choice == '1':
        #     add_occupant_names(OCCUPANTS_FILEPATH)
        if choice == '2':
            rank_chores(OCCUPANTS_FILEPATH, CHORES_FILEPATH, CHORE_RANKINGS_FILEPATH
        )
            break
        elif choice == '3':
            add_or_remove_chores(CHORES_FILEPATH)
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid selection. Please choose again.")



if __name__ == "__main__":
    # FIXME this should be removed once frontend works, this should only be imported as a module
    main()
