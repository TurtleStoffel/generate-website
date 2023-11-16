import os
import re
import subprocess
import yaml

from pathlib import Path
from typing import Optional

class MarkdownSourceFile:
    def __init__(self, source_path, config):
        self.source_path = source_path
        self.config = config
    
    def get_relative_url(self):
        filename = Path(self.source_path).stem
        parent_folder = Path(self.source_path).parent
        # Index files are automatically resolved as folders when loading a URL
        if filename == "index":
            # Ignore self-referential folder when defining URLs
            if parent_folder == Path('.'):
                return ''
            else:
                return f'{parent_folder}/'
        else:
            return f'{parent_folder}/{filename}'
    
    def get_permalink_mapping(self):
        with open(self.source_path, 'r') as f:
            content = f.read()
        
        permalink = get_permalink(content)

        if permalink:
            return {
                'permalink': f'/{permalink}',
                'url': f'/{self.get_relative_url()}'
            }
    
    def get_relative_destination_path(self):
        return f'{Path(self.source_path).parent}/{Path(self.source_path).stem}.html'
    
    def write(self):
        destination_path = f'{self.config.WEBSITE_DESTINATION_FOLDER}/{self.get_relative_destination_path()}'

        os.makedirs(Path(destination_path).parent, exist_ok=True)

        file_content = self._compile()

        with open(destination_path, 'w') as f:
            f.write(file_content)

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
        
        # Prepare Markdown file
        input = _change_markdown_link_pages_prefix(input)
        input = self._set_canonical_url(input)
        input = re.sub(r'^<!--.*?-->', '', input, flags=re.DOTALL | re.MULTILINE)
        
        return compile_markdown_string(input, self.config.TEMPLATE)

    """
    Add Canonical URL to Markdown Metadata section
    """
    def _set_canonical_url(self, content: str):
        canonical_url = f'{self.config.URL_PREFIX}/{self.get_relative_url()}'
        canonical_url_html = f'<link rel="canonical" href="{canonical_url}">'
        content = re.sub(r'\A---(.*?)---', rf'--- \1canonical_url: {canonical_url_html}\n---', content, flags=re.DOTALL | re.MULTILINE)
        return content
        

def compile_markdown_string(content: str, template):
    result = subprocess.run(
        ["pandoc", "--template", template, "--wrap=none", "-f", "gfm-tex_math_dollars"],
        input=content,
        text=True,
        stdout=subprocess.PIPE
    )

    return result.stdout

"""
Returns Permalink from Metadata in the file if present, otherwise returns None
"""
def get_permalink(content: str) -> Optional[str]:
    match = re.search(r'---(.*?)---', content, flags = re.MULTILINE | re.DOTALL)

    if not match:
        return None
    else:
        return yaml.safe_load(match.group(1)).get('permalink')

"""
Change Markdown link format from local .md file (starting with '/') to corresponding pages on the
website by stripping its suffix.

Suffix for standard pages is '.md'    /some/page.md         => /some/page
Suffix for index pages is 'index.md'  /some/folder/index.md => /some/folder/
"""
def _change_markdown_link_pages_prefix(content: str):
    # Strip suffix for index pages
    content = re.sub(r'^(\[\d+\]: )(/.*/)index.md$', r'\1\2', content, flags=re.MULTILINE)
    # Strip suffix for other pages
    return re.sub(r'^(\[\d+\]: )(/.*).md$', r'\1\2', content, flags=re.MULTILINE)
