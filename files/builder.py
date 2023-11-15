from .image_file import CopyFile
from .markdown_source_file import MarkdownSourceFile
from .source_file import SourceFile

def build_file_instance(file_path, type, config) -> SourceFile:
    if type == 'text':
        return MarkdownSourceFile(file_path, config)
    elif type == 'copy':
        return CopyFile(file_path, config)
