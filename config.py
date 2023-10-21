import yaml
import os

from pathlib import Path

source_folder = Path(__file__).parent

with open(f'{source_folder}/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

URL_PREFIX = config['url_prefix']
ROOT_DIR = os.path.expanduser(config['root_dir'])
WEBSITE_DESTINATION_FOLDER = os.path.expanduser(config['website_destination_folder'])
TEMPLATE = os.path.expanduser(config['template'])

FILES_TO_PROCESS = config['files_to_process']
