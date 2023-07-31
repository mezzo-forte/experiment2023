import os 
import json

def create_dir_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def create_if_not_exists(path, default_content):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(json.dumps(default_content))
    return path

path_data_folder = create_dir_if_not_exists(os.path.join(os.getcwd(), 'data'))
path_subjects_folder = create_dir_if_not_exists(os.path.join(path_data_folder, 'subjects'))
path_groups_folder = create_dir_if_not_exists(os.path.join(path_data_folder, 'groups'))
path_info = create_if_not_exists(os.path.join(path_data_folder, 'info.json'), {})
path_complex1 = os.path.join(os.getcwd(), 'complex1.json')
path_complex2 = os.path.join(os.getcwd(), 'complex2.json')
path_simple1 = os.path.join(os.getcwd(), 'simple1.json')
path_simple2 = os.path.join(os.getcwd(), 'simple2.json')
path_unpaid1 = os.path.join(os.getcwd(), 'unpaid1.json')
path_unpaid2 = os.path.join(os.getcwd(), 'unpaid2.json')


