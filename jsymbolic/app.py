import os
import logging
import subprocess
import shlex
from multiprocessing import Pool
from pathlib import Path
from jsymbolic.utils import cd

try:
    from tqdm import tqdm
except ImportError:
    logging.warning("Install tqdm with 'pip install tqdm'")
    tqdm = list


class Command(object):
    def __init__(self, path: str, ram: int, country: str, jsymbolic_path: str, xml_values_output: str = "values.xml", xml_definitions_output: str = "definitions.xml",
                 arff: bool = False, csv: bool = False, window_length: int = None, window_overlap_fraction: float = None, processed: bool = False):
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
        self.processed = processed

    def get(self) -> str:
        command = f"java -Xmx{self.ram}g " \
                  f"-Duser.country={self.country} " \
                  f' -jar "{self.jsymbolic_path}" ' \
                  f"{'-arff ' if self.arff else ''}" \
                  f"{'-csv ' if self.csv else ''}" \
                  f'"{self.path}" "{self.xml_values_output}" "{self.xml_definitions_output}" ' \
                  f"{self.window_length if self.window_length else ''} {self.window_overlap_fraction if (self.window_length and self.window_overlap_fraction) else ''}"
        return command


class App(object):
    def __init__(self, jar: str, ram: int = 6, country: str = 'EN'):
        self.jsymbolic_path = Path(jar)
        self.working_dir = self.jsymbolic_path.parent
        self.config_path = Path.joinpath(self.working_dir, "jSymbolicDefaultConfigs.txt")
        self.ram = ram
        self.country = country
        self.validate()
        self.command: Command = Command(path="", ram=ram, country=country, jsymbolic_path=self.jsymbolic_path.name)
        self.thread_pool = []

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

    def output_exists(self, csv: bool = False, arff: bool = False) -> bool:
        # Check for CSV file
        if csv:
            csv_path = str(self.command.xml_values_output).replace('.xml', '.csv')
            if not Path(csv_path).exists():
                logging.debug(f"{csv_path} is missing")
                return False

        # Check for ARFF file
        if arff:
            arff_path = str(self.command.xml_values_output).replace('.xml', '.arff')
            if not Path(arff_path).exists():
                logging.debug(f"{arff_path} is missing")
                return False

        # Check for XML file
        xml_path = self.command.xml_values_output
        if not Path(xml_path).exists():
            logging.debug(f"{xml_path} is missing")
            return False

        return True

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
                        self.command.xml_values_output = Path(collection).joinpath(f"{name}.xml").as_posix()
                    else:
                        self.command.xml_values_output = Path(collection).joinpath(f"{name}_{xml_values_output}").as_posix()
                    if skip_processed:
                        if self.output_exists(csv=csv, arff=arff):
                            self.command.processed = True
                        else:
                            self.command.processed = False
                    self.command.path = Path(collection).joinpath(file).as_posix()
                    self.execute_command(self.command)
        else:
            self.command.path = path
            self.execute_command(self.command)
        print("jSymbolic processing completed!")




    def execute_command(self, command: Command):
        """Run the current configuration
        Added parameters will overwrite the configuration"""
        if command.processed:
            logging.debug(f"Command already processed, skipping")
            return
        with cd(self.working_dir.as_posix()):
            logging.debug(f"cwd: {os.getcwd()}")
            command_string: str = command.get()
            logging.debug(f"Executing: {command_string}")
            process = subprocess.run(shlex.split(command_string),
                                     stdout=subprocess.PIPE,
                                     universal_newlines=True)
            #logging.debug(process.stdout)

class ThreadMeister9000(App):
    """Experimental"""
    def __init__(self, *args, thread_count=4, **kwargs):
        super(ThreadMeister9000, self).__init__(*args, **kwargs)
        self.thread_count = thread_count
        logging.warning("Threading is experimental!")

    def run(self, path: str, xml_values_output: str = "values.xml", xml_definitions_output: str = "definitions.xml",
            arff: bool = False, csv: bool = False, window_length: int = None, window_overlap_fraction: float = None,
            per_file: bool = True, skip_processed: bool = True):
        assert per_file, "per_file must be set to True for multi-threaded running"
        self.command.arff = arff
        self.command.csv = csv
        self.command.window_length = window_length
        self.command.window_overlap_fraction = window_overlap_fraction
        self.command.xml_values_output = Path(path).joinpath(xml_values_output).as_posix()
        self.command.xml_definitions_output = Path(path).joinpath(xml_definitions_output).as_posix()
        collection_files = {}
        for (dirpath, dirnames, filenames) in os.walk(path):
            collection_files[dirpath] = filenames

        # Collect tasks
        files = []
        tasks = []
        for collection, files in collection_files.items():
            files = [file for file in files if file.endswith(".midi") or file.endswith(".mid")]
            for file in files:
                name = file.replace(".mid", "").replace(".midi", "")
                if xml_values_output == "values.xml":
                    self.command.xml_values_output = Path(collection).joinpath(f"{name}.xml")
                else:
                    self.command.xml_values_output = Path(collection).joinpath(f"{name}_{xml_values_output}")
                if skip_processed:
                    if self.output_exists(csv=csv, arff=arff):
                        continue
                self.command.path = Path(collection).joinpath(file).as_posix()
                tasks.append(self.command)

        # Run thread pool
        pool = Pool(self.thread_count)
        for _ in tqdm(pool.imap_unordered(self.execute_command, tasks), total=len(files)):
            pass
        pool.close()  # POOL'S CLOSED
        pool.join()

        print("jSymbolic processing completed!")







