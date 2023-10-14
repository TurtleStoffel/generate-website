import config
import os

from pathlib import Path

class SourceFile:
    def write(self):
        destination_path = f'{config.WEBSITE_DESTINATION_FOLDER}/{self.get_relative_destination_path()}'

        os.makedirs(Path(destination_path).parent, exist_ok=True)

        file_content = self._compile()

        with open(destination_path, 'w') as f:
            f.write(file_content)
    
    def get_relative_url(self):
        raise NotImplementedError()
    
    def get_relative_destination_path(self):
        raise NotImplementedError()

    def _compile(self):
        raise NotImplementedError()


"""
Source file that is stored on disk
"""
class PhysicalSourceFile(SourceFile):
    def __init__(self, source_path: str):
        self.source_path = source_path


"""
Source file that is generated in memory
"""
class VirtualSourceFile(SourceFile):
    pass
