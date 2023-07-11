import os

def run_app(app_name='', project_name=''):
    to_run = ""
    if app_name == '':
        to_run = project_name
    else:
        to_run = app_name

    return to_run