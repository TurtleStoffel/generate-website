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

    def test_get_permalink_from_metadata_if_present(self):
        content = """
---
title: some-random-title
permalink: /some-random-permalink
breadcrumbs:
  - name: home
    url: /
---

# Random title
"""

        permalink = markdown_source_file.get_permalink(content)

        self.assertEqual(permalink, '/some-random-permalink')

    def test_get_permalink_from_metadata_returns_none_if_not_present(self):
        content = """
---
title: some-random-title
breadcrumbs:
  - name: home
    url: /
---

# Random title
"""

        permalink = markdown_source_file.get_permalink(content)

        self.assertEqual(permalink, None)
    
    def test_change_markdown_link_pages_prefix_folder(self):
        content = "[5]: /test/something/index.md"
        result = markdown_source_file._change_markdown_link_pages_prefix(content)

        self.assertEqual(result, "[5]: /test/something/")

    def test_change_markdown_link_pages_prefix_file(self):
        content = "[5]: /test/something/content.md"
        result = markdown_source_file._change_markdown_link_pages_prefix(content)

        self.assertEqual(result, "[5]: /test/something/content")

if __name__ == '__main__':
    unittest.main()
