"""
Author: Connie Williamson
Date: 03/3/2024

This file represents the tests for the log in module. 
"""
import unittest
import os
import csv
from login import *

# adds ability to easily compare a CSV when changed by these functions
# Source for idea: https://stackoverflow.com/questions/57097257/whats-the-best-way-to-unit-test-functions-that-handle-csv-files
test_file = "csvs/logintest.csv"

def setUpCSV(occupants):
    with open(test_file, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(occupants)

def tearDownCSV():
    os.remove(test_file)

class TestCreateUser(unittest.TestCase):
    def sub_test_csv_lines(self, contents):
        with open(test_file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for x in range(0, len(contents)):
                if x == 0:
                    self.assertEqual(next(reader), contents[x])
                else: 
                    uid_trimmed_row = next(reader)[1:]
                    self.assertEqual(uid_trimmed_row, contents[x][1:])
            
    def test_create_first_user(self):
        """Create the first user in the system as a simulation of Haus being started for the first time"""
        expected_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"]
        ]
        self.assertEqual(True, create_user("A", "XYZ", test_file))
        self.sub_test_csv_lines(expected_contents)
        tearDownCSV()

    def test_create_unique_user(self):
        """Create the second user in the system, where the username doesn't already exist"""
        start_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"]
        ]
        expected_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"],
            ["MOCK-UID", "B", "HKJ"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(True, create_user("B", "HKJ", test_file))
        self.sub_test_csv_lines(expected_contents)
        tearDownCSV()

    def test_create_non_unique_user(self):
        """Attempt and return error when attempting to create a user who already exists"""
        start_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"],
            ["MOCK-UID", "B", "HKJ"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(False, create_user("B", "HKJ", test_file))
        self.sub_test_csv_lines(start_contents)
        tearDownCSV()

class TestDeleteUser(unittest.TestCase):
    def sub_test_csv_lines(self, contents):
        with open(test_file, 'r') as csv_file:
            reader = csv.reader(csv_file)
            for x in range(0, len(contents)):
                if x == 0:
                    self.assertEqual(next(reader), contents[x])
                else: 
                    uid_trimmed_row = next(reader)[1:]
                    self.assertEqual(uid_trimmed_row, contents[x][1:])

    def test_delete_only_user(self):
        """Delete one user in the system, leaving an occupants file with no users."""
        start_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"]
        ]
        expected_contents = [
            ["Occupant UID", "Username", "Password"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(True, delete_user("A", "XYZ", test_file))
        self.sub_test_csv_lines(expected_contents)
        tearDownCSV()

    def test_delete_user_others_remain(self):
        """Delete one user in the system, leaving an occupants file with other users left untouched."""
        start_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"],
            ["MOCK-UID", "B", "HKJ"]
        ]
        expected_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "B", "HKJ"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(True, delete_user("A", "XYZ", test_file))
        self.sub_test_csv_lines(expected_contents)
        tearDownCSV()

    def test_delete_invalid_credentials(self):
        """Attempt and fail to delete because of incorrect password"""
        start_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"]
        ]
        expected_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(False, delete_user("A", "HKJ", test_file))
        self.sub_test_csv_lines(expected_contents)
        tearDownCSV()


    def test_delete_invalid_user_does_not_exist(self):
        """Attempt and fail to delete because user does not exist"""
        start_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"]
        ]
        expected_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(False, delete_user("C", "XYZ", test_file))
        self.sub_test_csv_lines(expected_contents)
        tearDownCSV()


class TestLogInUser(unittest.TestCase):
    def test_valid_login(self):
        """Attempt a valid login with valid credentials"""
        start_contents = [
                ["Occupant UID", "Username", "Password"],
                ["MOCK-UID", "A", "XYZ"],
                ["MOCK-UID", "B", "HKJ"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(True, log_in_user("A", "XYZ", test_file))
        tearDownCSV()

    def test_invalid_username(self):
        """Attempt an invalid login, where the username is not a real username"""
        start_contents = [
                ["Occupant UID", "Username", "Password"],
                ["MOCK-UID", "A", "XYZ"],
                ["MOCK-UID", "B", "HKJ"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(False, log_in_user("C", "XYZ", test_file))
        tearDownCSV()

    def test_invalid_password(self):
        """Attempt an invalid login, where the password is incorrect for a given username"""
        start_contents = [
                ["Occupant UID", "Username", "Password"],
                ["MOCK-UID", "A", "XYZ"],
                ["MOCK-UID", "B", "HKJ"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(False, log_in_user("A", "HKJ", test_file))
        tearDownCSV()

    def test_blank_login(self):
        """Attempt an invalid login where the information given is blank"""
        start_contents = [
                ["Occupant UID", "Username", "Password"],
                ["MOCK-UID", "A", "XYZ"],
                ["MOCK-UID", "B", "HKJ"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(False, log_in_user("", "", test_file))
        tearDownCSV()


class TestVerifyUserExists(unittest.TestCase):
    def test_user_does_exist_returns_true(self):
        start_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"],
            ["MOCK-UID", "B", "HKJ"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(True, verify_user_exists("A", test_file))
        tearDownCSV()

    def test_user_does_not_exist_returns_false(self):
        start_contents = [
            ["Occupant UID", "Username", "Password"],
            ["MOCK-UID", "A", "XYZ"],
            ["MOCK-UID", "B", "HKJ"]
        ]
        setUpCSV(start_contents)
        self.assertEqual(False, verify_user_exists("C", test_file))
        tearDownCSV()