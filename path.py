import os

# Get the absolute path of the current script
#current_file_path = os.path.abspath(__file__)

# Go one level up to find the project root
#project_root = os.path.dirname(os.path.dirname(current_file_path))

#print("Project Root Path:", project_root)

import database.context_manager
print(dir(database.context_manager))
