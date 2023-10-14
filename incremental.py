import os
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import config

from files.markdown_source_file import MarkdownSourceFile

class EventHandler(FileSystemEventHandler):
    def on_created(self, event):
        self.handle_markdown_file(event)
    
    def on_modified(self, event):
        self.handle_markdown_file(event)
    
    def handle_markdown_file(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')

        if '.md' in event.src_path:
            print('Compiling Markdown file')
            relative_path = os.path.relpath(event.src_path)
            markdown_source_file = MarkdownSourceFile(relative_path)
            markdown_source_file.write()

if __name__ == "__main__":
    os.chdir(os.path.expanduser(config.ROOT_DIR))

    path = '.'
    print(f'start watching directory {path!r}')
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()