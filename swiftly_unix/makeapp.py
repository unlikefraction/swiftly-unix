import os
import configparser
from swiftly_unix.config import CONFIG_FILE

def makeapp(app_name, venv_location):
    if '-' in app_name:
        raise Exception("Not a valid app name. App names can not contain '-'")
    
    # Split the app_name into parts
    app_parts = app_name.split('.')
    
    # Set the initial directory to the parent directory of the venv_location
    current_dir = os.path.dirname(venv_location)
    
    # Create directories for each part in app_parts
    for part in app_parts:
        current_dir = os.path.join(current_dir, part)
        os.makedirs(current_dir, exist_ok=True)
    
    # Create the __init__.py, __main__.py, app_name.py, and tests.py files in the final directory
    # Only create the files if they do not already exist
    if not os.path.exists(os.path.join(current_dir, '__init__.py')):
        with open(os.path.join(current_dir, '__init__.py'), 'w') as f:
            f.write(f'from .{app_parts[-1]} import *')
    
    if not os.path.exists(os.path.join(current_dir, '__main__.py')):
        with open(os.path.join(current_dir, '__main__.py'), 'w') as f:
            f.write(f'from .{app_parts[-1]} import *\n\n# Run the code from {app_parts[-1]}.py here')
    
    # Read the configuration file to determine whether to create a class or a function
    config = configparser.ConfigParser()
    config.read(os.path.join(venv_location, '..', CONFIG_FILE))
    object_oriented = config.getboolean('DEFAULT', 'OBJECT_ORIENTED')
    
    if not os.path.exists(os.path.join(current_dir, f'{app_parts[-1]}.py')):
        with open(os.path.join(current_dir, f'{app_parts[-1]}.py'), 'w') as f:
            if object_oriented:
                # Convert the app_name to CamelCase
                class_name = ''.join(word.title() for word in app_parts[-1].split('_'))
                f.write(f'class {class_name}:\n    def __init__(self):\n        pass')
            else:
                f.write(f'def {app_parts[-1]}():\n    pass')
    
    if not os.path.exists(os.path.join(current_dir, 'tests.py')):
        with open(os.path.join(current_dir, 'tests.py'), 'w') as f:
            f.write('# May all your tests pass :)')
