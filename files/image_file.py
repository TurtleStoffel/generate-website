import os
import shutil

from pathlib import Path

import config

from .source_file import PhysicalSourceFile

"""
File that is copied from it's original location to the destination without any changes
"""
class CopyFile(PhysicalSourceFile):
    def __init__(self, source_path: str):
        # Relative source and destination path are the same for image files
        super().__init__(source_path)
    
    def write(self):
        destination_path = f'{config.WEBSITE_DESTINATION_FOLDER}/{self.source_path}'
        os.makedirs(Path(destination_path).parent, exist_ok=True)

        shutil.copy(self.source_path, destination_path)