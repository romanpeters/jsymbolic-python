import os
import logging
import csv
import re
import shutil
import time
from pathlib import Path


class FileItem(object):
    """Representation of an individual file
            can flatten itself and append its info to a CSV file"""
    def __init__(self, path: str, index: int, csv_file: str = "preprocessor_changes.csv"):
        self.path = Path(path)
        self.csv_file = csv_file
        self.index = index
        self.name = self.path.name
        self.collection = self.path.parent.name
        self.flat_name = self.flatten(self.name)
        self.flat_collection = self.flatten(self.collection)
        self.output_name = f"{self.index}-{self.flat_collection}-{self.flat_name}"

    @staticmethod
    def flatten(name):
        """Removes special characters"""
        flatter = name.lower()
        flatter = flatter.replace(' ', '_')

        regex_filter = re.compile(r"[^a-zA-Z_.]")
        flat_name = regex_filter.sub('', flatter)

        logging.info(f"{name} -> {flat_name}")
        return flat_name

    def append_csv(self):
        """Writes its info to CSV"""
        with open(self.csv_file, 'a') as file:
            csv_writer = csv.writer(file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([self.index, self.name, self.output_name])


class PreProcessor(object):
    """The PreProcessor can move and copy FileItem objects
            it works with directories as well as single files"""
    def __init__(self, input_path: str, output_path: str = None, copy: bool = True, recursive: bool = True, group=False):
        # Make aware if permanent changes will be made
        if not copy:
            logging.warning("Copy is set to false, original file names will be overwritten!")
            assert not output_path, "Output path given but unused"
        else:
            assert copy and output_path, "Copy is set to true, an output path must be provided"

        self.run_id = int(time.time())
        self.csv_file = f"preprocessor_changes{self.run_id}.csv"
        self.input_path = Path(input_path)
        self.output_path = Path(output_path) if output_path else Path(input_path).parent
        self.copy = copy
        self.recursive = recursive
        self.current_index = 1


    def create_output_dir(self):
        logging.info(f"Creating output directory at {self.output_path.as_posix()}")
        os.makedirs(self.output_path.as_posix())

    def create_csv_file(self):
        with open(self.csv_file, 'w+') as file:
            csv_writer = csv.writer(file, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow(["index", "input name", "output name"])

    def run(self):
        if not self.copy:
            time.sleep(0.1)
            if not input("Overwrite file name? y/n ").lower()[0] == 'y':
                return
        if not self.output_path.exists():
            self.create_output_dir()
        if self.input_path.is_dir():
            self._change_collection()
        else:
            self._change_file(self.input_path)

    def _change_file(self, file_path: str):
        # Only MIDI files
        file_path_obj = Path(file_path)
        if not file_path_obj.is_file() or file_path_obj.suffix.lower() not in [".mid", ".midi"]:
            logging.warning(f"Skipped {file_path_obj.as_posix()} because it is not a MIDI file")
            return

        file_item = FileItem(path=file_path, index=self.current_index, csv_file=self.csv_file)

        dest_path = self.output_path.joinpath(file_item.output_name).as_posix()
        logging.info(f'renaming "{file_path}" -> "{dest_path}"')

        if not self.copy:
            shutil.move(file_path, dest_path)
        else:
            try:
                shutil.copy(file_path, dest_path)
            except shutil.SameFileError:
                logging.warning(f"Overwriting existing file {dest_path}")
                shutil.move(file_path, dest_path)
        file_item.append_csv()
        self.current_index += 1

    def _change_collection(self):
        # Collect all the paths
        collection_files = {}
        for (dirpath, dirnames, filenames) in os.walk(self.input_path):
            collection_files[dirpath] = filenames
            if not self.recursive:  # only files from the top dir if recursive=False
                break
        from pprint import pprint
        print(collection_files)

        # change files
        for collection, files in collection_files.items():
            for file in files:
                self._change_file(Path(collection).joinpath(file).as_posix())
