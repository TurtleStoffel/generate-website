import glob

import files

class FileGroup:
    def __init__(self, input_dict: dict):
        self.glob = input_dict['glob']
        type = input_dict['type']
        root = input_dict.get('root', None)

        resolved_file_paths = glob.glob(self.glob, recursive=True)
        self.files = [files.build_file_instance(file_path, type) for file_path in resolved_file_paths]

        if type == 'code-base':
            assert(root)
            self.files.append(files.IndexFile(self.files, root))
    
    def parse(self):
        for file in self.files:
            file.write()
    
    """
    Get all relative URLs of files in the file group.
    In case the file-group is a code-base, it will also contain the index.html file for the source
    """
    def get_relative_urls(self):
        return [file.get_relative_url() for file in self.files if not isinstance(file, files.CopyFile)]
