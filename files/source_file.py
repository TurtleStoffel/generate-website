import os

from pathlib import Path

class SourceFile:
    def __init__(self, source_path: str, config):
        self.source_path = source_path
        self.config = config

    def write(self):
        destination_path = f'{self.config.WEBSITE_DESTINATION_FOLDER}/{self.get_relative_destination_path()}'

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
