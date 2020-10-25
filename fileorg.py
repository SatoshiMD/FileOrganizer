#!/usr/bin/python

import os
import shutil
import time
import argparse
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler, PatternMatchingEventHandler


_extensions = {
    "IMAGES": [".jpeg", ".jpg", ".tiff", ".gif", ".bmp", ".png", ".bpg", "svg",
               ".heif", ".psd"],
    "VIDEOS": [".avi", ".flv", ".wmv", ".mov", ".mp4", ".webm", ".vob", ".mng",
               ".qt", ".mpg", ".mpeg", ".3gp"],
    "DOCUMENTS": [".oxps", ".epub", ".pages", ".docx", ".doc", ".fdf", ".ods",
                  ".odt", ".pwi", ".xsn", ".xps", ".dotx", ".docm", ".dox",
                  ".rvg", ".rtf", ".rtfd", ".wpd", ".ppt",
                  "pptx"],
    "DATA": [".csv", ".xls", ".xlsx"],
    "ARCHIVES": [".a", ".ar", ".cpio", ".iso", ".tar", ".gz", ".rz", ".7z",
                 ".dmg", ".rar", ".xar", ".zip", ".DS_Store", ".bz2"],
    "AUDIO": [".aac", ".aa", ".aac", ".dvf", ".m4a", ".m4b", ".m4p", ".mp3",
              ".msv", "ogg", "oga", ".raw", ".vox", ".wav", ".wma"],
    "PLAINTEXT": [".txt", ".in", ".out"],
    "SUBTITLES": [".srt"],
    "PDF": [".pdf"],
    "CODE": [".ipynb", ".sh", ".py", ".xml", ".html5", ".html", ".htm", ".xhtml", ".css", ".scss", ".sass", ".java", ".sql", ".python-version"],
    "EXE": [".exe"],
    "JUNKS": [".spec", ".lock", ".toml", ".torrent", ".msi", ".ini", ".appx"]
}

class FileWatch(object):
    def __init__(self, path):
        self.__watch_path__ = path
        self.observer = Observer()

    def run(self):
        event_handler = Handler() 
        self.observer.schedule(event_handler, self.__watch_path__, recursive = True) 
        self.observer.start() 
        try: 
            while True: 
                time.sleep(5) 
        except: 
            self.observer.stop() 
            print("Observer Stopped") 
  
        self.observer.join() 


class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        print('on_modified')

    def on_created(self, event):
        print("on_created - % s." % event.src_path)
        
        if not event.is_directory:
            Oepration.move_files(event.src_path.split('\\')[0])
        else:
            print(event.src_path)
            Oepration.move_dir(event.src_path)


class Oepration(object):
    @classmethod
    def move_dir(cls, target):
        try:
            path, dir = target.split('\\')
            detination = os.path.join(os.path.join(path, 'OTHERS'), path)
            shutil.move(target, detination)
        except Exception as e:
            print(str(e))
            return str(e)

    @classmethod
    def move_files(cls, path):
        try:
            items = [item for item in os.listdir(path) if '.' in item]
            exts = _extensions.items()
            for item in items:
                time.sleep(1)
                res = [k for k, v in exts if '.' + item.split('.')[-1].lower() in v]
                if len(res) > 0:
                    target = os.path.join(path, item)
                    detination = os.path.join(path, res[0])
                    is_moved = shutil.move(target, detination)
                    print(is_moved, item)
        except Exception as e:
            print(str(e))
            return str(e)


if __name__ == "__main__":
    # Parsing argument
    parser = argparse.ArgumentParser()

    # Adding optional argument
    parser.add_argument("-d", "--dir", help = "Watch Directory")
    args = parser.parse_args()

    # Setting default values
    path = args.dir if args.dir else '.'

    # Initializing the dir
    for d in _extensions.keys():
        if not os.path.exists(os.path.join(path, d)):
            os.mkdir(os.path.join(path, d))

    if not os.path.exists(os.path.join(path, 'OTHERS')):
        os.mkdir(os.path.join(path, 'OTHERS'))

    # Moving files
    Oepration.move_files(path)

    # Starting watch
    watch = FileWatch(path) 
    watch.run() 