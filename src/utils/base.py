import os

def return_app_dir(current_location):
    return os.path.dirname(os.path.dirname(os.path.dirname(current_location)))

