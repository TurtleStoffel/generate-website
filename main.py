import os
import shutil
import yaml

import config

from get_files_to_process import get_files_to_process
from files.markdown_source_file import MarkdownSourceFile

"""
Sorts the provided file paths and writes them to a sitemap
"""
def generate_sitemap(markdown_files: list[MarkdownSourceFile]):
    relative_urls = [file.get_relative_url() for file in markdown_files]
    
    urls = [f'{config.URL_PREFIX}{relative_url}\n' for relative_url in relative_urls]

    # An explicit sort is required at the end, because wildcards in the input can cause unsorted
    # results:
    # E.g.,
    # - *.py -> extends to main.py and source.py
    # - resource/template.html -> would have to be in between main.py and source.py
    sorted_urls = sorted(urls)

    sitemap_path = f'{config.WEBSITE_DESTINATION_FOLDER}/sitemap.txt'

    with open(sitemap_path, 'w') as f:
        f.writelines(sorted_urls)

def generate_permalink_mapping(markdown_files: list[MarkdownSourceFile]):
    mappings = []
    for file in markdown_files:
        mapping = file.get_permalink_mapping()
        if mapping:
            mappings.append({
                'permalink': mapping['permalink'],
                'url': mapping['url']
            })
    
    # Validate uniqueness of permalinks
    uniqueness_set = set()
    for mapping in mappings:
        permalink = mapping['permalink']
        assert(permalink not in uniqueness_set)
        uniqueness_set.add(permalink)
    
    sorted_mappings = sorted(mappings, key = lambda mapping: mapping['permalink'])
    
    with open(config.PERMALINK_MAPPING_OUTPUT, 'w') as f:
        f.writelines(yaml.dump(sorted_mappings))

if __name__ == '__main__':
    os.chdir(config.ROOT_DIR)

    copy_files, markdown_files = get_files_to_process()

    if os.path.exists(config.WEBSITE_DESTINATION_FOLDER):
        shutil.rmtree(config.WEBSITE_DESTINATION_FOLDER)

    for file in copy_files:
        file.write()
    
    file_to_permalink_mapping = {}
    for file in markdown_files:
        mapping = file.get_permalink_mapping()
        if mapping:
            file_to_permalink_mapping[mapping['file']] = mapping['permalink']
    
    for file in markdown_files:
        file.write(file_to_permalink_mapping)

    generate_sitemap(markdown_files)
    generate_permalink_mapping(markdown_files)
