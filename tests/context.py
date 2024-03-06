"""
Context for Unit Testing
Author: Alex JPS
Date: 03/05/2024

This file starts the Python module search at the project root.
"""

import sys, os
this_folder = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.abspath(os.path.join(this_folder, "..")))