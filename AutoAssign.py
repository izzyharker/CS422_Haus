"""
Automatic Chore Assignment and Repetition
Author: Alex JPS
Date: 03/05/2024

This file represents the automatic chore assignment system, which decides who to give each unassigned chore
based on previous workload and future expected workload.

This also handles generating new instances of chores which repeat.
"""

# other modules in the software
import DataInput
from DataInput import CHORE_STATUS, Chore

# python libraries
import re
from datetime import datetime, timedelta, date

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
    DataInput.update_chore_by_object(chore)

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

def renew_repeating_chores() -> None:
    """
    Renew all repeating chores that are ready to be renewed.
    (i.e. they are both completed and the deadline has passed)

    This also marks these chores as renewed such that they will never be renewed again.
    (instead, the new instance of the chore will be renewed later, when it is completed)
    """
    def increment_id(old_id: str) -> str:
        """
        Given a Chore ID in one of the two following formats, increment the number indicating repetitions.
        uuid
        uuid(repetitions)
        """
        # make sure the old id is in a valid format (prevent undefined behavior)
        pattern = r'^[\w-]+(\(\d+\))?$'
        if not re.match(pattern, old_id):
            raise ValueError(f"Invalid id format: {old_id}")
        # no parentheses? add them
        if "(" not in old_id:
            return f"{old_id}(1)"
        # get the unique uuid part and the parentheses part
        uuid_part, parentheses_part = old_id.split("(")
        parentheses_part = parentheses_part.split(")")[0]
        # increment the number and return the new id
        repetition = int(parentheses_part) + 1
        return f"{uuid_part}({repetition})"

    # Get all repeating chores that are ready for renewal
    chores_to_renew: list[Chore] = DataInput.get_chores_by_filters(
        repeating_only=True,
        status=CHORE_STATUS.COMPLETED,
        max_deadline_date=date.today()
    )

    # renew each applicable chore
    for chore in chores_to_renew:
        # mark the chore as renewed
        chore.status = CHORE_STATUS.RENEWED
        DataInput.update_chore_by_object(chore)
        # edit the chore attributes to be used for the new instance
        assert isinstance(chore.completion_date, date)  # Python linter freaks out without this line
        chore.deadline_date = chore.completion_date + timedelta(days=chore.frequency+1)
        chore.status = CHORE_STATUS.UNASSIGNED
        chore.assignee_id = None
        chore.completion_date = None
        chore.id = increment_id(chore.id)
        # add the new chore to the database
        DataInput.new_chore_by_object(chore)

    # assign the renewed chores
    assign_unassigned_chores()