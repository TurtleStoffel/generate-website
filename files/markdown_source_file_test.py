import unittest

from . import markdown_source_file

class MarkdownSourceFile(unittest.TestCase):
    def test_should_update_markdown_links_to_correct_format(self):
        content = """
[4]: /some/folder/index.md
[3]: /some/page.md
"""

        result = markdown_source_file._change_markdown_link_pages_prefix(content)

        self.assertEqual(result, """
[4]: /some/folder/
[3]: /some/page
""")

if __name__ == '__main__':
    unittest.main()
