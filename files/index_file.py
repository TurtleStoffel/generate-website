from .markdown_source_file import compile_markdown_string
from .source_file import VirtualSourceFile, PhysicalSourceFile

class IndexFile(VirtualSourceFile):
    def __init__(self, files: list[PhysicalSourceFile], root: str):
        self.files = files.copy()
        self.root = root
    
    def get_relative_url(self):
        return f'{self.root}'
    
    def get_relative_destination_path(self):
        return f'{self.root}/index.html'
    
    def _compile(self):
        if not self.root:
            raise RuntimeError("A code-base did not have a root defined")

        html = '---\ntitle: Index\n---\n'
        for file in self.files:
            stripped_file_name = file.source_path.removeprefix(f'{self.root}/')
            html += f'<a href="/{file.get_relative_url()}">{stripped_file_name}</a></br>\n'
        
        return compile_markdown_string(html)