import os
import logging
import subprocess
import shlex
from pathlib import Path
from jsymbolic.utils import cd

try:
    from tqdm import tqdm
except ImportError:
    tqdm = list


class App(object):
    def __init__(self, jar: str, ram: int = 6, country: str = 'EN'):
        self.jsymbolic_path = Path(jar)
        self.working_dir = self.jsymbolic_path.parent
        self.config_path = Path.joinpath(self.working_dir, "jSymbolicDefaultConfigs.txt")
        self.ram = ram
        self.country = country
        self.validate()
        self.command: Command = Command(path="", ram=ram, country=country, jsymbolic_path=self.jsymbolic_path.name)

        with open(self.config_path.absolute().as_posix(), "r") as f:
            self.config = f.read().splitlines()

    def validate(self):
        """Checks if paths exist"""
        if not self.jsymbolic_path.exists():
            logging.warning(f"jSymbolic jar not found at {self.jsymbolic_path.absolute()}")
        if not self.config_path.exists():
            logging.warning(f"Config not found at {self.config_path}. Set it manually using set_config()")

    def set_config(self, path: str):
        """Manually set config file for jSymbolic"""
        self.config_path: Path = Path(path)
        self.validate()

    def run_config(self, config_path: str = None):
        """Run using a config file with the paths of the MIDI files
        Unless you have such a config file, you're probably better of using run() instead.
        """
        command = f"java -Duser.country={self.country} -Xmx{self.ram}g " \
                  f"-jar {self.jsymbolic_path} " \
                  f"-configrun {config_path if config_path else self.config_path}"
        print(command)
        raise NotImplementedError

    def get_config(self):
        """Returns the current config"""
        return '\n'.join(self.config)

    def run(self, path: str, xml_values_output: str = "values.xml", xml_definitions_output: str = "definitions.xml",
            arff: bool = False, csv: bool = False, window_length: int = None, window_overlap_fraction: float = None,
            per_file: bool = False, skip_processed: bool = True):
        self.command.arff = arff
        self.command.csv = csv
        self.command.window_length = window_length
        self.command.window_overlap_fraction = window_overlap_fraction
        self.command.xml_values_output = Path(path).joinpath(xml_values_output).as_posix()
        self.command.xml_definitions_output = Path(path).joinpath(xml_definitions_output).as_posix()
        if per_file:
            collection_files = {}
            for (dirpath, dirnames, filenames) in os.walk(path):
                collection_files[dirpath] = filenames

            for collection, files in collection_files.items():
                files = [file for file in files if file.endswith(".midi") or file.endswith(".mid")]
                for file in tqdm(files):
                    name = file.replace(".mid", "").replace(".midi", "")
                    if xml_values_output == "values.xml":
                        self.command.xml_values_output = Path(collection).joinpath(f"{name}.xml")
                    else:
                        self.command.xml_values_output = Path(collection).joinpath(f"{name}_{xml_values_output}")
                    if skip_processed:
                        # Skip execution if there's already an xml file
                        if Path(self.command.xml_values_output).exists():
                            continue
                    self.command.path = Path(collection).joinpath(file).as_posix()
                    self.execute_command()
        else:
            self.command.path = path
            self.execute_command()

    def execute_command(self):
        """Run the current configuration
        Added parameters will overwrite the configuration"""
        with cd(self.working_dir.as_posix()):
            logging.debug(f"cwd: {os.getcwd()}")
            command: str = self.command.get()
            logging.debug(f"Executing: {command}")
            process = subprocess.run(shlex.split(command),
                                     stdout=subprocess.PIPE,
                                     universal_newlines=True)
            logging.debug(process.stdout)

    # def create_config(self, path: str, xml_values_output: str = "values.xml", xml_definitions_output: str = "definitions.xml",
    #                   arff: bool = False, csv: bool = False, window_length: int = None, window_overlap_fraction: float = None):
    #
    #     config = f"""
    #     <output_files>
    #         feature_values_save_path={xml_values_output}
    #         feature_definitions_save_path={xml_definitions_output}
    #     <input_files>
    #         {path}
    #         """

class Command(object):
    def __init__(self, path: str, ram: int, country: str, jsymbolic_path: str, xml_values_output: str = "values.xml", xml_definitions_output: str = "definitions.xml",
                 arff: bool = False, csv: bool = False, window_length: int = None, window_overlap_fraction: float = None):
        self.path = path
        self.ram = ram
        self.country = country
        self.jsymbolic_path = jsymbolic_path
        self.xml_values_output = xml_values_output
        self.xml_definitions_output = xml_definitions_output
        self.arff = arff
        self.csv = csv
        self.window_length = window_length
        self.window_overlap_fraction = window_overlap_fraction

    def get(self) -> str:
        command = f"java -Xmx{self.ram}g " \
                  f"-Duser.country={self.country} " \
                  f' -jar "{self.jsymbolic_path}" ' \
                  f"{'-arff ' if self.arff else ''}" \
                  f"{'-csv ' if self.csv else ''}" \
                  f'"{self.path}" "{self.xml_values_output}" "{self.xml_definitions_output}" ' \
                  f"{self.window_length if self.window_length else ''} {self.window_overlap_fraction if (self.window_length and self.window_overlap_fraction) else ''}"
        return command







