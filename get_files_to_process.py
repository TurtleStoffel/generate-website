import config

from file_group import CopyFileGroup, MarkdownFileGroup

"""
Reads file groups to be processed and validates if files are ordered to make it easier to see if
URLs have changed in the resulting Sitemap.
"""
def get_file_groups_to_process() -> tuple[list[CopyFileGroup], list[MarkdownFileGroup]]:
    # Force the list of files to be sorted to avoid a messy input file
    if not _is_sorted([file['glob'] for file in config.FILES_TO_PROCESS]):
        raise RuntimeError("List of files to process must be sorted")

    copy_file_groups = [CopyFileGroup(raw_files) for raw_files in config.FILES_TO_PROCESS if raw_files['type'] == 'copy']
    markdown_file_groups = [MarkdownFileGroup(raw_files) for raw_files in config.FILES_TO_PROCESS if raw_files['type'] == 'text']
    
    return copy_file_groups, markdown_file_groups

def _is_sorted(list):
    return all(a <= b for a, b in zip(list, list[1:]))