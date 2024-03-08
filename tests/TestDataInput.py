"""
Author: Alex JPS
Date: 03/05/2024

This file provides a comprehensive test suite for the DataInput.py module.

In PyCharm, set the Python Tests configuration to use the 'tests' directory as working dir.
If running via command line, any working dir is fine.
"""

# fix import path
import Context

# modules
import unittest
from datetime import date
import os
import shutil

# module to test
import DataInput

# logging configuration
import logging

logging.basicConfig(level=logging.DEBUG)


class TestChore(unittest.TestCase):
    """
    This class provides unit tests for the Chore class constructor.
    """

    def test_chore_constructor(self):
        """
        This method tests the Chore class constructor
        """
        # dict simulating a row from the chores.csv file,
        # hence all values are strings
        some_uid: str = DataInput.generate_uid()
        csv_chore_row: dict = {
            "Chore ID": some_uid,
            "Chore Name": "Dishes",
            "Description": "Wash the dishes",
            "Category": "Kitchen",
            "Expected Duration": "30",
            "Status": "unassigned",
            "Assignee ID": "",
            "Deadline Date": "2024-03-05",
            "Completion Date": "",
        }
        # create a Chore object from the csv_chore_row
        chore = DataInput.Chore(csv_chore_row)

        # check that the Chore object was created correctly
        expected = [
            (chore.id, some_uid),
            (chore.name, "Dishes"),
            (chore.description, "Wash the dishes"),
            (chore.category, "Kitchen"),
            (chore.expected_duration, 30),
            (chore.status, DataInput.CHORE_STATUS.UNASSIGNED),
            (chore.assignee_id, None),
            (chore.deadline_date, date(2024, 3, 5)),
            (chore.completion_date, None)
        ]
        for attribute, expected_value in expected:
            self.assertEqual(attribute, expected_value)
        logging.debug("Passed test_chore_constructor")


class TestGetFunctions(unittest.TestCase):
    """
    This class provides unit tests for functions
    that get (but do not change) database information.
    """

    def setUp(self):
        """
        Rename database files in the csvs directory to preserve them.
        They will be restored to their original names after testing.
        Replace them with mockup database files for testing.
        """
        # preserve the original database CSV files
        self.replacements = [
            ("./csvs/chores.csv", "./csvs/tmp_chores.csv"),
            ("./csvs/occupants.csv", "./csvs/tmp_occupants.csv"),
        ]
        for old_name, new_name in self.replacements:
            try:
                os.rename(old_name, new_name)
            except FileNotFoundError:
                logging.debug(f"No file to preserve: {old_name}")
        # use mockup files
        shutil.copyfile("./tests/mock_chores.csv", "./csvs/chores.csv")
        shutil.copyfile("./tests/mock_occupants.csv", "./csvs/occupants.csv")
        logging.debug("Replaced files with mockups in setUp")

    def tearDown(self):
        """
        Remove the csvs/chores.csv generated during these unit tests,
        Replace it with the version available prior to testing
        """
        for old_name, new_name in self.replacements:
            try:
                os.replace(new_name, old_name)
            except FileNotFoundError:
                logging.debug(f"No file to restore: {old_name}")
        logging.debug("Restored files in tearDown")

    def test_get_chore_by_id(self):
        """
        This method tests the get_chore_by_id function
        """
        # there is already a chore with this id in our mock chores file
        chore_id: str = "7cb263c2-52f5-4077-971e-491d3d19ed29"
        # get the corresponding chore
        chore: DataInput.Chore = DataInput.get_chore_by_id(chore_id)
        # make sure each attribute of the chore is as expected
        expected_matches = [
            (chore.id, chore_id),
            (chore.name, "Vacuum"),
            (chore.description, "Vacuum all carpets and rugs"),
            (chore.category, "General"),
            (chore.expected_duration, 30),
            (chore.status, DataInput.CHORE_STATUS.UNASSIGNED),
            (chore.assignee_id, None),
            (chore.deadline_date, date(2024, 3, 11)),
            (chore.completion_date, None)
        ]
        for attribute, expected_value in expected_matches:
            self.assertEqual(attribute, expected_value)
        logging.debug("Passed test_get_chore_by_id")

    def test_get_chores_by_filters_all(self):
        """
        This method tests the chores_by_filters function with no filters.
        We assume that Chore objects contain the right information.
        We only check that the IDs of the returned chores match expectations.
        """
        # get all chores
        all_chores: list[DataInput.Chore] = DataInput.get_chores_by_filters()
        # check that the IDs of all chores are as expected
        expected_ids: list[str] = [
            "f79759a1-47ef-42c4-9879-c353c3329f50",
            "b2c10fdc-f023-4360-9bf6-d62122333039",
            "9e4fe3a0-aa47-40e0-9efd-eb4f62c5f922",
            "7cb263c2-52f5-4077-971e-491d3d19ed29",
            "575e2770-e278-4dc5-95a3-e918ecebdc31"
        ]
        # make sure each id appears exactly once in the returned chores
        self.assertEqual(len(all_chores), len(expected_ids))
        ids_found: set[str] = set()
        for chore in all_chores:
            self.assertIn(chore.id, expected_ids)
            if chore.id in ids_found:
                self.fail("Duplicate chore returned by get_chores_by_filters")
            ids_found.add(chore.id)
        # make sure every id was found
        self.assertEqual(ids_found, set(expected_ids))
        logging.debug("Passed test_get_chores_by_filters_all")

    def test_get_chores_by_filters_status1(self):
        """
        This method tests the chores_by_filters function with a status filter.
        We assume that Chore objects contain the right information.
        We only check that the IDs of the returned chores match expectations.
        """
        # get all chores with status "unassigned"
        unassigned_chores: list[DataInput.Chore] = \
            DataInput.get_chores_by_filters(status=DataInput.CHORE_STATUS.UNASSIGNED)
        # check that the IDs of all chores are as expected
        expected_ids: list[str] = [
            "7cb263c2-52f5-4077-971e-491d3d19ed29"
        ]
        # make sure each id appears exactly once in the returned chores
        self.assertEqual(len(unassigned_chores), len(expected_ids))
        ids_found: set[str] = set()
        for chore in unassigned_chores:
            self.assertIn(chore.id, expected_ids)
            if chore.id in ids_found:
                self.fail("Duplicate chore returned by get_chores_by_filters")
            ids_found.add(chore.id)
        # make sure every id was found
        self.assertEqual(ids_found, set(expected_ids))
        logging.debug("Passed test_get_chores_by_filters_status")

    def test_get_chores_by_filters_status2(self):
        """
        This method tests the chores_by_filters function with a status filter.
        We assume that Chore objects contain the right information.
        We only check that the IDs of the returned chores match expectations.
        """
        # get all chores with status "assigned"
        assigned_chores: list[DataInput.Chore] = \
            DataInput.get_chores_by_filters(status=DataInput.CHORE_STATUS.ASSIGNED)
        # check that the IDs of all chores are as expected
        expected_ids: list[str] = [
            "f79759a1-47ef-42c4-9879-c353c3329f50",
            "9e4fe3a0-aa47-40e0-9efd-eb4f62c5f922",
            "575e2770-e278-4dc5-95a3-e918ecebdc31"
        ]
        # make sure each id appears exactly once in the returned chores
        self.assertEqual(len(assigned_chores), len(expected_ids))
        ids_found: set[str] = set()
        for chore in assigned_chores:
            self.assertIn(chore.id, expected_ids)
            if chore.id in ids_found:
                self.fail("Duplicate chore returned by get_chores_by_filters")
            ids_found.add(chore.id)
        # make sure every id was found
        self.assertEqual(ids_found, set(expected_ids))
        logging.debug("Passed test_get_chores_by_filters_status")

    def test_get_chores_by_filters_min_deadline_date(self):
        """
        This method tests the chores_by_filters function with a min_deadline_date filter.
        We assume that Chore objects contain the right information.
        We only check that the IDs of the returned chores match expectations.
        """
        # get all chores with deadline after or including 2024-03-12
        filtered_chores: list[DataInput.Chore] = \
            DataInput.get_chores_by_filters(min_deadline_date=date(2024, 3, 12))
        # check that the IDs of all chores are as expected
        expected_ids: list[str] = [
            "f79759a1-47ef-42c4-9879-c353c3329f50",
            "b2c10fdc-f023-4360-9bf6-d62122333039",
            "9e4fe3a0-aa47-40e0-9efd-eb4f62c5f922",
        ]
        # make sure each id appears exactly once in the returned chores
        self.assertEqual(len(filtered_chores), len(expected_ids))
        ids_found: set[str] = set()
        for chore in filtered_chores:
            self.assertIn(chore.id, expected_ids)
            if chore.id in ids_found:
                self.fail("Duplicate chore returned by get_chores_by_filters")
            ids_found.add(chore.id)
        # make sure every id was found
        self.assertEqual(ids_found, set(expected_ids))
        logging.debug("Passed test_get_chores_by_filters_min_deadline_date")

    def test_get_chores_by_filters_max_deadline_date(self):
        """
        This method tests the chores_by_filters function with a max_deadline_date filter.
        We assume that Chore objects contain the right information.
        We only check that the IDs of the returned chores match expectations.
        """
        # get all chores with deadline before or including 2024-03-12
        filtered_chores: list[DataInput.Chore] = \
            DataInput.get_chores_by_filters(max_deadline_date=date(2024, 3, 12))
        # check that the IDs of all chores are as expected
        expected_ids: list[str] = [
            "f79759a1-47ef-42c4-9879-c353c3329f50",
            "7cb263c2-52f5-4077-971e-491d3d19ed29",
            "575e2770-e278-4dc5-95a3-e918ecebdc31"
        ]
        # make sure each id appears exactly once in the returned chores
        self.assertEqual(len(filtered_chores), len(expected_ids))
        ids_found: set[str] = set()
        for chore in filtered_chores:
            self.assertIn(chore.id, expected_ids)
            if chore.id in ids_found:
                self.fail("Duplicate chore returned by get_chores_by_filters")
            ids_found.add(chore.id)
        # make sure every id was found
        self.assertEqual(ids_found, set(expected_ids))
        logging.debug("Passed test_get_chores_by_filters_max_deadline_date")

    def test_get_user_ids(self):
        """
        This method tests the get_user_ids function.
        """
        # get all user ids
        user_ids: list[str] = DataInput.get_user_ids()
        # check that the user ids are as expected
        expected_ids: list[str] = [
            "95454c41-dc2f-451e-97b5-1d53b31cfa16",
            "c55b4c05-2f74-4bfb-8077-03192dd74aab",
            "0c9ef357-f312-4f85-93c0-16672244a2b5"
        ]
        # make sure each id appears exactly once in the returned user ids
        self.assertEqual(len(user_ids), len(expected_ids))
        ids_found: set[str] = set()
        for user_id in user_ids:
            self.assertIn(user_id, expected_ids)
            if user_id in ids_found:
                self.fail("Duplicate user ID returned by get_user_ids")
            ids_found.add(user_id)
        # make sure every id was found
        self.assertEqual(ids_found, set(expected_ids))
        logging.debug("Passed test_get_user_ids")


class TestSetFunctions(unittest.TestCase):
    """
    This class provides unit tests for functions that change database
    information (they do not necessarily contain the word "set").
    """

    def setUp(self):
        """
        Rename database files in the csvs directory to preserve them.
        They will be restored to their original names after testing.
        Replace them with mockup database files for testing.
        """
        # preserve the original database CSV files
        self.replacements = [
            ("./csvs/chores.csv", "./csvs/tmp_chores.csv"),
            ("./csvs/occupants.csv", "./csvs/tmp_occupants.csv"),
        ]
        for old_name, new_name in self.replacements:
            try:
                os.rename(old_name, new_name)
            except FileNotFoundError:
                logging.debug(f"No file to preserve: {old_name}")
        # use mockup files
        shutil.copyfile("./tests/mock_chores.csv", "./csvs/chores.csv")
        shutil.copyfile("./tests/mock_occupants.csv", "./csvs/occupants.csv")
        logging.debug("Replaced files with mockups in setUp")

    def tearDown(self):
        """
        Remove the csvs/chores.csv generated during these unit tests,
        Replace it with the version available prior to testing
        """
        for old_name, new_name in self.replacements:
            try:
                os.replace(new_name, old_name)
            except FileNotFoundError:
                logging.debug(f"No file to restore: {old_name}")
        logging.debug("Restored files in tearDown")

    def test_update_chore(self):
        """
        This method tests the update_chore function.
        We check the attributes of a chore, update them, and check again.
        """
        # confirm an attribute of a chore from the mock chores file
        # we will not check every single attribute
        chore: DataInput.Chore = DataInput.get_chore_by_id("7cb263c2-52f5-4077-971e-491d3d19ed29")
        print("The chore is: ", chore)
        self.assertEqual(chore.name, "Vacuum")
        self.assertEqual(chore.status, DataInput.CHORE_STATUS.UNASSIGNED)
        self.assertEqual(chore.assignee_id, None)
        # update the chore
        chore.name = "Hoover"
        chore.status = DataInput.CHORE_STATUS.ASSIGNED
        chore.assignee_id = "95454c41-dc2f-451e-97b5-1d53b31cfa16"
        DataInput.update_chore(chore)
        # now check again to make sure the attributes in the chores file are as expected
        updated_chore: DataInput.Chore = DataInput.get_chore_by_id("7cb263c2-52f5-4077-971e-491d3d19ed29")
        self.assertEqual(updated_chore.name, "Hoover")
        self.assertEqual(updated_chore.status, DataInput.CHORE_STATUS.ASSIGNED)
        self.assertEqual(updated_chore.assignee_id, "95454c41-dc2f-451e-97b5-1d53b31cfa16")
        logging.debug("Passed test_update_chore")

if __name__ == "__main__":
    unittest.main()
