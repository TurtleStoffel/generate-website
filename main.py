import os
import shutil
import yaml

import config

from get_files_to_process import get_file_groups_to_process
from file_group import FileGroup


"""
Sorts the provided file paths and writes them to a sitemap
"""
def generate_sitemap(file_groups: list[FileGroup]):
    relative_urls = []
    for file_group in file_groups:
        relative_urls.extend(file_group.get_relative_urls())
    
    urls = [f'{config.URL_PREFIX}/{relative_url}\n' for relative_url in relative_urls]

    # An explicit sort is required at the end, because wildcards in the input can cause unsorted
    # results:
    # E.g.,
    # - *.py -> extends to main.py and source.py
    # - resource/template.html -> would have to be in between main.py and source.py
    sorted_urls = sorted(urls)

    sitemap_path = f'{config.WEBSITE_DESTINATION_FOLDER}/sitemap.txt'

    with open(sitemap_path, 'w') as f:
        f.writelines(sorted_urls)

def generate_permalink_mapping(file_groups: list[FileGroup]):
    mappings = []
    for file_group in file_groups:
        mappings.extend(file_group.get_permalink_mapping())
    
    with open(config.PERMALINK_MAPPING_OUTPUT, 'w') as f:
        f.writelines(yaml.dump(mappings))

if __name__ == '__main__':
    os.chdir(os.path.expanduser(config.ROOT_DIR))

    copy_files, markdown_files = get_file_groups_to_process()

    if os.path.exists(config.WEBSITE_DESTINATION_FOLDER):
        shutil.rmtree(config.WEBSITE_DESTINATION_FOLDER)

    for file_group in copy_files:
        file_group.parse()
    
    for file_group in markdown_files:
        file_group.parse()

    generate_sitemap(markdown_files)
    generate_permalink_mapping(markdown_files)
