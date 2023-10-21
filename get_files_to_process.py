import config

from file_group import FileGroup

"""
Reads file groups to be processed and validates if files are ordered to make it easier to see if
URLs have changed in the resulting Sitemap.
"""
def get_file_groups_to_process() -> list[FileGroup]:
    files_objects = [FileGroup(raw_files) for raw_files in config.FILES_TO_PROCESS]

    # Force the list of files to be sorted to avoid a messy input file
    if not _is_sorted([file.glob for file in files_objects]):
        raise RuntimeError("List of files to process must be sorted")
    
    return files_objects

def _is_sorted(list):
    return all(a <= b for a, b in zip(list, list[1:]))