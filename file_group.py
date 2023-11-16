import glob

import config

from files.builder import build_file_instance
from files.image_file import CopyFile

class MarkdownFileGroup:
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
    """
    def get_relative_urls(self):
        return [file.get_relative_url() for file in self.files]
    
    def get_permalink_mapping(self):
        mappings = []
        for file in self.files:
            mapping = file.get_permalink_mapping()
            if mapping:
                mappings.append(mapping)
        
        return mappings

class CopyFileGroup:
    def __init__(self, input_dict: dict):
        self.glob = input_dict['glob']
        type = input_dict['type']

        resolved_file_paths = glob.glob(self.glob, recursive=True)
        self.files = [build_file_instance(file_path, type, config) for file_path in resolved_file_paths]
    
    def parse(self):
        for file in self.files:
            file.write()
