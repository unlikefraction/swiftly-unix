import os
import subprocess
import configparser
from swiftly_unix.makeapp import makeapp
from swiftly_unix.gitignore import GITIGNORE
from swiftly_unix.config import CONFIG_FILE

def get_venv_location():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    project_name = config.get('DEFAULT', 'PROJECT_NAME')

    venv_name = f'venv{project_name}'
    venv_exists = os.path.exists(venv_name)

    if not venv_exists:
        subprocess.run(['python3', '-m', 'venv', venv_name])

        # Add the virtual environment to the .gitignore file
        if not os.path.exists('.gitignore'):
            with open('.gitignore', 'w') as f:
                f.write(GITIGNORE)
        with open('.gitignore', 'a') as f:
            f.write(f'\n{venv_name}/')

    venv_location = os.path.abspath(venv_name)
    return venv_location

def get_project_name():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    
    try:
        project_name = config.get('DEFAULT', 'PROJECT_NAME')
    except configparser.NoOptionError:
        # If the project name is not found in the config file, use the name of the current directory
        dir_name = os.path.basename(os.getcwd())
        # Replace any '-' characters with '_' to make it a valid Python module name
        project_name = dir_name.replace('-', '_')
        # Initialise the new project
        initialise(project_name, in_place=True)
    
    return project_name


def pull_changes(git_status):
    return 'Your branch is behind' in git_status

def check_new_packages(available_packages):
    with open('requirements.txt', 'r') as f:
        required_packages = f.read().splitlines()

    available_packages = set(available_packages.split())
    required_packages = set(required_packages)

    return not required_packages.issubset(available_packages)

def is_repo(name):
    repo_markers = ["https://", "http://", ".git", "git@"]
    
    repo_check = [marker in name for marker in repo_markers]
    return True in repo_check

def clone_successful(git_clone):
    if "ERROR:" in git_clone or "fatal:" in git_clone:
        lines = git_clone.split('=')
        error_lines = [line for line in lines if line.startswith(("ERROR:", "fatal:"))]
        return ' '.join(error_lines)
    else:
        return True

def initialise(name, in_place=False):
    if is_repo(name):
        name = name.split('/')[-1].replace('.git', '')

    if not os.path.exists(name):
        os.makedirs(name)
    
    if not in_place:
        os.chdir(name)

    if not os.path.exists('requirements.txt'):
        with open('requirements.txt', 'w') as f:
            pass
        
    if not os.path.exists('env.py'):
        with open('env.py', 'w') as f:
            pass
        
    if not os.path.exists('__init__.py'):
        with open('__init__.py', 'w') as f:
            pass

    if not os.path.exists(CONFIG_FILE):
        config = configparser.ConfigParser()
        config['DEFAULT'] = {
                                'PROJECT_NAME': name,
                                'OBJECT_ORIENTED': False,
                            }
        
        with open(CONFIG_FILE, 'w') as f:
            config.write(f)

    venv_location = get_venv_location()
    
    makeapp(name, venv_location)

    return venv_location
