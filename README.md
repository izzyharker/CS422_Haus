# HAUS
Project 2 for CS 422: Software Methodologies at the University of Oregon. Completed Winter 2024.  

Authors: Izzy Harker, Andrew Rehmann, Alex Peterson Santos, Connie Williamson, Carter Young

Description: Prototype of a chore tracking app for roommates. Includes unique user account features, global administrative capabilities, and automatic chore scheduling. The goal of this app is to offload the burden of chore tracking and enforcing onto the software, instead of a roommate having to keep track of it.

## Installation
This software runs on both Python and JavaScript, with local servers for both environments. Please note that this has not been tested on Linux, so we cannot guarantee success within that environment.

### Mac
1. Download and install Python 3.12 from python.org. If you already have a python environment, proceed to step 2.

2. Run the following command in the Terminal to install pip (for package management). If you already have pip installed, proceed to step 3 (under "Both"):

```python -m ensurepip --upgrade```

### Windows
1. Download and install Python 3.12 from python.org. If you already have a python environment, proceed to step 2.

2. Run the following command in the Terminal to install pip (for package management). If you already have pip installed, proceed to step 3 (under "Both"):

```C:> py -m ensurepip --upgrade```

### Both
3. Install Flask (dependency for the system) by running the following command in the same terminal as step 2:

```pip install flask```

4. Download and install Node 20.11.1 from https://nodejs.org/en. At the moment, this is the LTS version of the software. 

5. Navigate to the "CS422_Haus/Frontend/" directory of the project. Run the command 

```npm install```

to install the required React dependencies for the project. The exact dependencies are listed in `Frontend/package-lock.json`. 

All other dependencies are part of the Python standards library and do not need to be installed separately. 

## Running
1) In a terminal window, navigate to the main directory of the project:

```echo $pwd```

```PATH_TO_FOLDER/CS422_Haus/```

2) Run 

```python flask_integration.py```

to start the Flask server
3) Open a new terminal window. 
4) Navigate to the "Frontend" directory within the project

```echo $pwd```

```PATH_TO_FOLDER/CS422_Haus/Frontend/```

5) Run 

```npm run dev``` 

to start the React server.
6) Cmd + click on the displayed link to open the window in a browser. 

## Troubleshooting
It is possible that no chores will show up on the home screen, especially for a new user. This most likely only indicates that the user has no current assigned chores, and is not a cause for alarm. 

If actions do not work as described in this document and the programmer's documentation, please double check that both the Flask server and React (Vite) server are actively running.

The login is standardized across all browser windows using local storage, so if you would like to test the system with multiple, either log in and out or use separate browsers. 

