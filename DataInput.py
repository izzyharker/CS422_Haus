"""
Author: Carter Young
Date: 02/24/24

This file represents the data input module. It also enables all data input to be stored in the appropriate file type.
Inputs:
- House, Roommate, and Chore definitions from user

Outputs:
- .csv files for Houses, Roommates, and Chores

"""

import csv
import uuid


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
                # File is empty or headers don't match:
                # Move to the start of the file to overwrite or prepend headers
                file.seek(0, 0)
                writer = csv.writer(file)
                writer.writerow(headers)

                # If only the headers were incorrect, we need to preserve the rest of that data
                if existing_headers:
                    # Move writer cursor to EoF
                    file.seek(0, 2)
                    # Write what was read as the first row back into the file
                    writer.writerow(existing_headers)

    except FileNotFoundError:
        # File does not exist, create new file with headers
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

    num_people = input("Enter the number of people living there: ")

    return haus_name, haus_type, num_people


def add_occupant_names(dwelling_file, occupants_file):
    """ Allows user to enter names of occupants in a given Haus. """
    house_uid = input("Enter the UID of the house: ").strip()
    # Verify the house UID exists
    num_occupants, found = verify_uid_and_get_occupants(dwelling_file, house_uid)
    if not found:
        print("House UID not found.")
        return

    occupant_name = input("Enter new occupant name (leave blank to finish): ")
    while occupant_name:
        occupant_uid = str(uuid.uuid4())  # Generate unique ID for new occupant
        save_occupant_names(occupants_file, house_uid, occupant_uid, occupant_name)
        print(f"Added {occupant_name} with UID {occupant_uid} to house {house_uid}.")
        occupant_name = input("Enter new occupant name (leave blank to finish): ")


def verify_uid_and_get_occupants(filename, uid):
    with open(filename, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == uid:  # Assuming UID is always in the first column
                return int(row[3]), True
    return 0, False


def save_occupant_names(filename, house_uid, occupant_uid, occupant_name):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([house_uid, occupant_uid, occupant_name])


def initialize_chores(chores_file):
    default_chores = [
        (1, "Dishes", "Wash and dry the dishes"),
        (2, "Laundry", "Wash, dry, and fold clothes"),
        (3, "Vacuum", "Vacuum all carpets and rugs"),
        (4, "Dusting", "Dust all surfaces"),
        (5, "Trash", "Take out the trash and recycling"),
        (6, "Bathroom", "Clean the toilets and showers"),
        (7, "Sweeping", "Sweep floors"),
        (8, "Mopping", "Mop floors")
    ]
    try:
        with open(chores_file, 'r') as file:
            pass
    except FileNotFoundError:
        with open(chores_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Chore ID', 'Chore Name', 'Description'])
            for chore in default_chores:
                writer.writerow(chore)


def rank_chores(occupants_file, chores_file, chore_rankings_file):
    house_uid = input("Enter the UID of the house for ranking chores: ").strip()
    occupants = retrieve_occupants_names_and_uids(occupants_file, house_uid)

    if not occupants:
        print("No occupants found for this UID.")
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
    for chore_id, chore_name, _ in chores:
        valid_rank = False
        while not valid_rank:
            rank = input(f"Rank for {chore_name} (0, 1, or 2): ").strip()
            if rank in ['0', '1', '2']:
                valid_rank = True
                rankings.append((house_uid, occupant_uid, chore_id, rank))
            else:
                print("Invalid rank. Please enter 0, 1, or 2.")
    save_chore_rankings(chore_rankings_file, rankings)


def retrieve_occupants_names_and_uids(occupants_file, house_uid):
    occupants = {}
    with open(occupants_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header
        for row in reader:
            if row[0] == house_uid:
                # Assuming the format is: House UID, Occupant UID, Occupant Name
                occupants[row[1]] = row[2]
    return occupants


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


def main():
    dwelling_file = 'hauses.csv'
    occupants_file = 'occupants.csv'
    chores_file = 'chores.csv'
    chore_rankings_file = 'chore_rankings.csv'

    # Initialize files
    ensure_csv_headers(occupants_file, ['House UID', 'Occupant UID', 'Occupant Name'])
    ensure_csv_headers(chore_rankings_file, ['Unique Key', 'Occupant Name', 'Chore ID', 'Rank'])
    initialize_chores(chores_file)

    # Main menu loop
    while True:
        print("\nMenu:")
        print("1. Add a new Haus")
        print("2. Add occupants to an existing Haus")
        print("3. Rank chores for a Haus")
        print("4. Exit")
        choice = input("Select an option (1/2/3/4): ")

        if choice == '1':
            name, dwelling_type, num_people = get_haus_info()
            unique_key = generate_uid()
            append_to_csv(dwelling_file, [unique_key, name, dwelling_type, num_people])
            print(f"New Haus added with unique key: {unique_key}")
            break
        elif choice == '2':
            add_occupant_names(dwelling_file, occupants_file)
        elif choice == '3':
            rank_chores(occupants_file, chores_file, chore_rankings_file)
            break
        elif choice == '4':
            print("Exiting program.")
            break
        else:
            print("Invalid selection. Please choose again.")


if __name__ == "__main__":
    main()
