import html
import re

from pathlib import Path

import config

from .source_file import PhysicalSourceFile

class CodeSourceFile(PhysicalSourceFile):
    def __init__(self, source_path):
        self.destination_path = f'{source_path}.html'
        super().__init__(source_path)
    
    def get_relative_destination_path(self):
        return self.destination_path
    
    def get_relative_url(self):
        return self.destination_path

    
    def _compile(self):
        with open(self.source_path, 'r') as f:
            content = html.escape(f.read())
        
        with open(config.TEMPLATE, 'r') as f:
            template = f.read()
        
        extension = Path(self.source_path).suffix
        if extension == ".ts":
            language_class = "language-typescript"
        elif extension == ".py":
            language_class = "language-python"
        elif extension == ".kt":
            language_class = "language-kotlin"
        else:
            language_class = ""
        
        content_with_html_tags = f'<pre><code class="{language_class}">{content}</code></pre>'
        
        # The order is important when generating the HTML file of the template, otherwise the title
        # would be replaced twice
        template = template.replace('$title$', Path(self.source_path).name)
        template = re.sub(r'\$\{ if\(breadcrumbs\) \}.*\$\{ endif \}', '', template, flags=re.DOTALL)
        template = template.replace('        <link rel="canonical" href="$canonical_url$">', '')
        template = template.replace('$body$', content_with_html_tags)

        return template