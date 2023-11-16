import glob

import config

from file_group import MarkdownFileGroup
from files.image_file import CopyFile

"""
Reads file groups to be processed and validates if files are ordered to make it easier to see if
URLs have changed in the resulting Sitemap.
"""
def get_file_groups_to_process() -> tuple[list[CopyFile], list[MarkdownFileGroup]]:
    # Force the list of files to be sorted to avoid a messy input file
    if not _is_sorted([file['glob'] for file in config.FILES_TO_PROCESS]):
        raise RuntimeError("List of files to process must be sorted")

    copy_file_groups = [_create_copy_files(raw_files) for raw_files in config.FILES_TO_PROCESS if raw_files['type'] == 'copy']
    copy_files = _flatten(copy_file_groups)
    markdown_file_groups = [MarkdownFileGroup(raw_files) for raw_files in config.FILES_TO_PROCESS if raw_files['type'] == 'text']
    
    return copy_files, markdown_file_groups

def _is_sorted(list):
    return all(a <= b for a, b in zip(list, list[1:]))

def _flatten(list: list[list[any]]):
    return [item for sublist in list for item in sublist]

def _create_copy_files(input_dict: dict):
    file_glob = input_dict['glob']
    resolved_file_paths = glob.glob(file_glob, recursive=True)
    return [CopyFile(file_path, config) for file_path in resolved_file_paths]

