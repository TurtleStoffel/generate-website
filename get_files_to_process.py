import yaml

from pathlib import Path

from file_group import FileGroup

"""
Reads file groups to be processed and validates if files are ordered to make it easier to see if
URLs have changed in the resulting Sitemap.
"""
def get_file_groups_to_process() -> list[FileGroup]:
    files_objects = [FileGroup(raw_files) for raw_files in _read_file()]

    # Force the list of files to be sorted to avoid a messy input file
    if not _is_sorted([file.glob for file in files_objects]):
        raise RuntimeError("List of files to process must be sorted")
    
    return files_objects

def _read_file() -> list[dict]:
    source_folder = Path(__file__).parent
    files_to_process_file = f'{source_folder}/resource/files-to-process.yaml'

    with open(files_to_process_file, 'r') as f:
        files = yaml.safe_load(f.read())
    
    return files

def _is_sorted(list):
    return all(a <= b for a, b in zip(list, list[1:]))