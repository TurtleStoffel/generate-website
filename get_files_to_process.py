import glob

import config
import util

from files.image_file import CopyFile
from files.markdown_source_file import MarkdownSourceFile

"""
Reads file groups to be processed and validates if files are ordered to make it easier to see if
URLs have changed in the resulting Sitemap.
"""
def get_file_groups_to_process() -> tuple[list[CopyFile], list[MarkdownSourceFile]]:
    # Force the list of files to be sorted to avoid a messy input file
    if not util.is_sorted([file['glob'] for file in config.FILES_TO_PROCESS]):
        raise RuntimeError("List of files to process must be sorted")

    copy_file_groups = [_create_copy_files(raw_files) for raw_files in config.FILES_TO_PROCESS if raw_files['type'] == 'copy']
    copy_files = util.flatten(copy_file_groups)
    markdown_file_groups = [_create_markdown_files(raw_files) for raw_files in config.FILES_TO_PROCESS if raw_files['type'] == 'text']
    markdown_files = util.flatten(markdown_file_groups)
    
    return copy_files, markdown_files

def _create_copy_files(input_dict: dict):
    file_glob = input_dict['glob']
    resolved_file_paths = glob.glob(file_glob, recursive=True)
    return [CopyFile(file_path, config) for file_path in resolved_file_paths]

def _create_markdown_files(input_dict: dict):
    file_glob = input_dict['glob']
    resolved_file_paths = glob.glob(file_glob, recursive=True)
    return [MarkdownSourceFile(file_path, config) for file_path in resolved_file_paths]
