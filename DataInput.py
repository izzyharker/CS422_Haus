"""
Author: Carter Young, Alex JPS
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
from enum import Enum
from datetime import datetime
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
    deadline_date: Union[datetime, None]
    completion_date: Union[datetime, None]

    def __init__(self, csv_chore_row: dict):
        """
        Constructor to create a Chore object based on a dict from a chore CSV row
        """
        self.name = csv_chore_row["Chore Name"]
        self.id = csv_chore_row["Chore ID"]
        self.description = csv_chore_row["Description"]
        self.category = csv_chore_row["Category"]
        self.expected_duration = csv_chore_row["Expected Duration"]
        self.status = CHORE_STATUS(csv_chore_row["Status"])
        self.assignee_id = csv_chore_row["Assignee ID"]
        self.deadline_date = datetime.strptime(csv_chore_row["Deadline Date"], DATE_FORMAT) \
            if csv_chore_row["Deadline Date"] else None
        self.completion_date = datetime.strptime(csv_chore_row["Completion Date"], DATE_FORMAT) \
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


def add_occupant_names(occupants_file):
    """ Allows user to enter names of occupants in a given Haus. """

    """
    # Removing option to add house (deprecated)
    house_uid = input("Enter the UID of the house: ").strip()
    # Verify the house UID exists
    num_occupants, found = verify_uid_and_get_occupants(dwelling_file, house_uid)
    if not found:
        print("House UID not found.")
        return
    """

    occupant_name = input("Enter new occupant name (leave blank to finish): ")
    while occupant_name:
        occupant_uid = str(uuid.uuid4())  # Generate unique ID for new occupant
        save_occupant_names(occupants_file, occupant_uid, occupant_name)
        print(f"Added {occupant_name} with UID {occupant_uid} to house.")
        occupant_name = input("Enter new occupant name (leave blank to finish): ")


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


def initialize_chores(chores_file):
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
        with open(chores_file, 'r') as file:
            pass
    except FileNotFoundError:
        with open(chores_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(CHORE_ATTRIBUTES)
            for chore in default_chores:
                writer.writerow(chore)


def rank_chores(occupants_file, chores_file, chore_rankings_file):
    """ This function allows users to rank chores """
    occupants = retrieve_occupants_names_and_uids(occupants_file)

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
    chores = list_chores(chores_file)
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

    save_chore_rankings(chore_rankings_file, rankings)


def retrieve_occupants_names_and_uids(occupants_file):
    occupants = {}
    with open(occupants_file, mode='r') as file:
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


def add_or_remove_chores(chores_file):
    """Allows users to add or remove chores from the list."""
    action = input("Do you want to add or remove a chore? (add/remove): ").lower()
    if action == 'add':
        add_chore(chores_file)
    elif action == 'remove':
        remove_chore(chores_file)
    else:
        print("Invalid action. Please enter 'add' or 'remove'.")


def add_chore(chores_file):
    """Adds a new chore to the chores list."""
    chore_name = input("Enter the name of the chore: ")
    description = input("Enter the chore description: ")
    category = input("Enter the chore category: ")
    expected_duration = input("Enter the estimated time to complete the chore (in minutes): ")
    chore_id = generate_uid()  # Using UUID for unique chore identifiers

    with open(chores_file, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            [chore_id, chore_name, description, category, expected_duration, CHORE_STATUS.UNASSIGNED.value, None, None,
             None])

    print(f"Chore '{chore_name}' added successfully.")


def remove_chore(chores_file):
    """Removes a chore from the chores list."""
    chore_name = input("Enter the name of the chore to remove: ")
    temp_chores = []
    chore_found = False

    with open(chores_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        headers = next(reader)  # Capture headers
        for row in reader:
            if row[1] != chore_name:  # Assuming chore name is in the second column
                temp_chores.append(row)
            else:
                chore_found = True

    if chore_found:
        with open(chores_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)  # Write the headers back
            writer.writerows(temp_chores)  # Write the remaining chores
        print(f"Chore '{chore_name}' removed successfully.")
    else:
        print("Chore not found.")


def list_chores(chores_file):
    chores = []
    with open(chores_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            chores.append(row)
    return chores


def save_chore_rankings(chore_rankings_file, rankings):
    with open(chore_rankings_file, mode='a', newline='') as file:
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
               min_completion_date: datetime = None,
               max_deadline_date : datetime = None) -> list[Chore]:
    """
    Return a list of Chore objects matching the given filters.
    The list will be empty if none of the chores in the database match.
    """
    matching_chores = []
    file = open(CHORES_FILEPATH, 'r')
    reader = csv.DictReader(file)
    for row in reader:
        if assignee_id and row["Assignee ID"] != assignee_id:
            continue
        if min_completion_date and row["Completion Date"] < min_completion_date:
            continue
        if max_deadline_date and row["Deadline Date"] > max_deadline_date:
            continue
        matching_chores.append(Chore(row))
    file.close()
    return matching_chores

def get_user_category_preferences(user_id: str) -> list[tuple[str, int]]:
    """
    Return a list of (category, preference) tuples for the given user_id.
    The preferences can be 0 (negative), 1 (neutral), or 2 (positive).
    """
    file = open('csvs/chore_rankings.csv', 'r')
    reader = csv.DictReader(file)
    preferences = []
    for row in reader:
        if row["Occupant UID"] == user_id:
            # TODO implement rankings based on category and not chore ID, and change "ranking" -> "preference"
            preferences.append((row["Chore UID"], row["Rank"]))
    file.close()
    return preferences

# TODO remove this once frontend works
def main():
    # dwelling_file = 'csvs/hauses.csv'
    occupants_file = 'csvs/occupants.csv'
    chores_file = 'csvs/chores.csv'
    chore_rankings_file = 'csvs/chore_rankings.csv'

    # Initialize files
    # ensure_csv_headers(dwelling_file, ['House Name', 'House Type', 'Num Occupants'])
    ensure_csv_headers(occupants_file, ['Occupant UID', 'Occupant Name'])
    ensure_csv_headers(chore_rankings_file, ['Occupant UID', 'Chore UID', 'Rank'])
    initialize_chores(chores_file)
    ensure_csv_headers(chores_file, CHORE_ATTRIBUTES)

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
        print("1. Add occupants to an existing Haus")
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
        if choice == '1':
            add_occupant_names(occupants_file)
        elif choice == '2':
            rank_chores(occupants_file, chores_file, chore_rankings_file)
            break
        elif choice == '3':
            add_or_remove_chores(chores_file)
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid selection. Please choose again.")



if __name__ == "__main__":
    # FIXME this should be removed once frontend works, this should only be imported as a module
    main()
