import os
import shutil

from pathlib import Path

"""
File that is copied from it's original location to the destination without any changes
"""
class CopyFile:
    def __init__(self, source_path: str, config):
        self.source_path = source_path
        self.config = config
    
    def write(self):
        destination_path = f'{self.config.WEBSITE_DESTINATION_FOLDER}/{self.source_path}'
        os.makedirs(Path(destination_path).parent, exist_ok=True)

        shutil.copy(self.source_path, destination_path)