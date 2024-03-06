"""
Automatic Chore Assignment
Author: Alex JPS
Date: 03/05/2024

This file represents the automatic chore assignment system, which decides who to give each unassigned chore
based on previous workload and future expected workload.

Inputs (obtained by interfacing with DataInput module):
- Work history of each user, currently unassigned chores

Outputs:
- Assignment decisions that keep the workload well distributed
"""

# imports
import DataInput
from DataInput import CHORE_STATUS, Chore
from datetime import datetime, timedelta

def assign_unassigned_chores() -> None:
    """
    Find unassigned chores and assign them to users based on workload.
    """
    # Check if there are any unassigned chores
    unassigned_chores = DataInput.get_chores_by_filters(status=CHORE_STATUS.UNASSIGNED)
    if not unassigned_chores:
        # No unassigned chores
        print("Called assign_chores() but no unassigned chores found")
        return
    # Get the workload of each user
    workloads = []
    for user_id in DataInput.get_user_ids():
        # append a (user_id, workload) tuple to the workloads list
        workloads.append((user_id, user_workload(user_id)))
    # Sort the chores by expected duration, descending
    unassigned_chores.sort(key=lambda x: x.expected_duration, reverse=True)
    for chore in unassigned_chores:
        # Assign the chore to the user with the lowest workload
        workloads.sort(key=lambda x: x[1])
        assign_chore(chore, workloads[0][0])
        # Update the workload of the user who was assigned the chore
        workloads[0] = (workloads[0][0], workloads[0][1] + chore.expected_duration)

def assign_chore(chore: Chore, assignee_id: str) -> None:
    """
    Assign a chore to a user.
    """
    # Update the Chore object's status and assignee_id
    chore.status = CHORE_STATUS.ASSIGNED
    chore.assignee_id = assignee_id
    # Update the database using DataInput
    DataInput.update_chore(chore)

def user_workload(user_id: str):
    """
    Calculate the workload of a given user within the past seven and next seven days.
    This is entirely based off of the work they are supposed to do, regardless of whether they have done it.
    """
    # Get chores from the desired timeframe
    week_ago = (datetime.today() - timedelta(days=7)).date()
    next_week = (datetime.today() + timedelta(days=7)).date()
    work_chores = DataInput.get_chores_by_filters(assignee_id=user_id, min_deadline_date=week_ago, max_deadline_date=next_week)
    # add up the time it takes to do each chore
    workload = 0
    for chore in work_chores:
        workload += chore.expected_duration
    return workload