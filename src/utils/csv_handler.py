import csv
from typing import List

def read_target_users(file_path: str) -> List[str]:
    """Read target users from CSV file."""
    target_users = []
    with open(file_path, 'r') as fl:
        dm_list = csv.reader(fl)
        for row in dm_list:
            target_users.append(row[0])
    return target_users
