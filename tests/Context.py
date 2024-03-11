"""
Context for Unit Testing
Author: Alex JPS
Date: 03/05/2024

This file starts the Python module search and file I/O from the project root.
"""

# modules
import sys
import os

# logging configuration
import logging
logging.basicConfig(level=logging.DEBUG)

# define the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# start Python module search from the project root
sys.path.insert(0, project_root)

# start file I/O from the project root
os.chdir(project_root)

logging.debug(f"Working in directory {os.getcwd()}")