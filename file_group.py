import glob

import config

from files.builder import build_file_instance
from files.image_file import CopyFile

class FileGroup:
    def __init__(self, input_dict: dict):
        self.glob = input_dict['glob']
        type = input_dict['type']

        resolved_file_paths = glob.glob(self.glob, recursive=True)
        self.files = [build_file_instance(file_path, type, config) for file_path in resolved_file_paths]
    
    def parse(self):
        for file in self.files:
            file.write()
    
    """
    Get all relative URLs of files in the file group.
    In case the file-group is a code-base, it will also contain the index.html file for the source
    """
    def get_relative_urls(self):
        return [file.get_relative_url() for file in self.files if not isinstance(file, CopyFile)]
