import glob

import config
import util

from files.image_file import CopyFile
from files.markdown_source_file import MarkdownSourceFile

"""
Reads file groups to be processed and validates if files are ordered to make it easier to see if
URLs have changed in the resulting Sitemap.
"""
def get_files_to_process() -> tuple[list[CopyFile], list[MarkdownSourceFile]]:
    # Force the list of files to be sorted to avoid a messy input file
    if not util.is_sorted([file['glob'] for file in config.FILES_TO_PROCESS]):
        raise RuntimeError("List of files to process must be sorted")
    
    copy_files = []
    markdown_files = []
    for file_group_definition in config.FILES_TO_PROCESS:
        file_glob = file_group_definition['glob']
        resolved_file_paths = glob.glob(file_glob, recursive=True)

        if file_group_definition['type'] == 'copy':
            copy_files.extend([CopyFile(file_path, config) for file_path in resolved_file_paths])
        
        elif file_group_definition['type'] == 'text':
            markdown_files.extend([MarkdownSourceFile(file_path, config) for file_path in resolved_file_paths])
    
    return copy_files, markdown_files
