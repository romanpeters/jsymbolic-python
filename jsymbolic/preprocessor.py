import os
import logging
from pathlib import Path

class FileItem(object):
    def __init__(self, path, index, csv_file):
        self.path = Path(path)
        self.csv_file =
        self.name = None


    def flatten(self):
        self.name = self.name.lower()

    def write(self):



class PreProcessor(object):
    def __init__(self, input_path: str, output_path: str = None, copy: bool = True, recursive: bool = True):
        # Make aware if permanent changes will be made
        if not copy:
            logging.warning("Copy is set to false, original file names will be overwritten!")
            assert not output_path, "Output path given but unused"
        else:
            assert copy and output_path, "Copy is set to true, an output path must be provided"

        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self.copy = copy
        self.recursive = recursive

    def run(self):
        if self.input_path.is_dir():
            self._change_collection()
        else:
            self._change_file()

    def _change_file(self):
        raise NotImplementedError

    def _change_collection(self):
        raise NotImplementedError


class Indexer(object):
    def __init__(self, ):
