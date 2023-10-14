import re
import subprocess

from pathlib import Path

import config

from .source_file import PhysicalSourceFile

class MarkdownSourceFile(PhysicalSourceFile):
    def __init__(self, source_path):
        super().__init__(source_path)
    
    def get_relative_url(self):
        filename = Path(self.source_path).stem
        parent_folder = Path(self.source_path).parent
        # Index files are automatically resolved as folders when loading a URL
        if filename == "index":
            # Ignore self-referential folder when defining URLs
            if parent_folder == Path('.'):
                return ''
            else:
                return f'{parent_folder}'
        else:
            return f'{parent_folder}/{filename}'
    
    def get_relative_destination_path(self):
        return f'{Path(self.source_path).parent}/{Path(self.source_path).stem}.html'

    """
    The source file is preprocessed by stripping all todo items in the form of
    <!--TODO
    (...)
    -->
    because the VSCode Markdown Preview does not support YAML metadata blocks and they don't stand out
    enough within the document.
    """
    def _compile(self):
        with open(self.source_path, 'r') as f:
            input = f.read()
        
        return compile_markdown_string(input)
        

def compile_markdown_string(content: str):
    content = _change_markdown_link_pages_prefix(content)
    stripped_input = re.sub(r'^<!--.*?-->', '', content, flags=re.DOTALL | re.MULTILINE)

    result = subprocess.run(
        ["pandoc", "--template", config.TEMPLATE, "--wrap=none", "-f", "markdown-tex_math_dollars-raw_tex"],
        input=stripped_input,
        text=True,
        stdout=subprocess.PIPE
    )

    return result.stdout

"""
Change Markdown link format from local .md file (starting with '/') to corresponding pages on the
website by stripping its suffix.

Suffix for standard pages is '.md'.
Suffix for index pages is '/index.md'.
"""
def _change_markdown_link_pages_prefix(content: str):
    # Strip suffix for index pages
    content = re.sub(r'^(\[\d+\]: )(/.*)/index.md$', r'\1 \2', content, flags=re.MULTILINE)
    # Strip suffix for other pages
    return re.sub(r'^(\[\d+\]: )(/.*).md$', r'\1 \2', content, flags=re.MULTILINE)
