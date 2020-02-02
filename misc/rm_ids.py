import os
import shutil
from pathlib import Path

def run():
    collection_files = {}
    for (dirpath, dirnames, filenames) in os.walk("."):
        collection_files[dirpath] = filenames

    # change files
    for collection, files in collection_files.items():
        for file_path in files:
            new_path = file_path
            splitted = new_path.split("-")
            if splitted[0].isdigit():
                new_path = "-".join(splitted[1:])



            print(file_path, "->", new_path)
            #shutil.move(file_path, new_path)

run()