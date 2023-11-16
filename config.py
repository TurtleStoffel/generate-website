import argparse
import yaml
import os

# Parse command line arguments
parser = argparse.ArgumentParser(
    description='Convert Markdown files to HTML'
)
parser.add_argument('config_file', help='Configuration file')
args = parser.parse_args()

# Load configuration
with open(args.config_file, 'r') as file:
    config = yaml.safe_load(file)

URL_PREFIX = config['url_prefix']
ROOT_DIR = os.path.expanduser(config['root_dir'])
WEBSITE_DESTINATION_FOLDER = os.path.expanduser(config['website_destination_folder'])
PERMALINK_MAPPING_OUTPUT = os.path.expanduser(config['permalink_mapping_output'])

TEMPLATE = os.path.expanduser(config['template'])

FILES_TO_PROCESS = config['files_to_process']
