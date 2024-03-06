"""
Author: Alex JPS
Date: 03/05/2024

This file provides a comprehensive test suite for the DataInput.py module.
"""

import context
import unittest
import DataInput


class TestChore(unittest.TestCase):
    """
    This class provides unit tests for the Chore class constructor.
    """

    def test_chore_constructor(self):
        """
        This method tests the Chore class constructor
        """
        pass


class TestGetFunctions(unittest.TestCase):
    """
    This class provides unit tests for functions
    that get (but do not change) database information.
    """
    pass

    def test_get_chore_by_id(self):
        """
        This method tests the get_chore_by_id function
        """
        pass

    def test_chores_by_filters(self):
        """
        This method tests the chores_by_filters function
        """
        pass

    def test_get_user_ids(self):
        """
        This method tests the get_user_ids function
        """
        pass


class TestSetFunctions(unittest.TestCase):
    """
    This class provides unit tests for functions that change database
    information (they do not necessarily contain the word "set").
    """

    def test_update_chore(self):
        """
        This method tests the update_chore function
        """
        pass
