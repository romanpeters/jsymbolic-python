import os
import logging
import subprocess
import shlex
from pathlib import Path
from contextlib import contextmanager


@contextmanager
def cd(newdir):
    """Safely change working directory"""
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)


class App(object):
    def __init__(self, jar: str, ram: int = 6, country: str = 'EN'):
        self.jsymbolic_path = Path(jar)
        self.working_dir = self.jsymbolic_path.parent
        self.config_path = Path.joinpath(self.working_dir, "jSymbolicDefaultConfigs.txt")
        self.ram = ram
        self.country = country
        self.validate()

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

    def get_config(self):
        """Returns the current config"""
        return '\n'.join(self.config)

    def run(self, path: str, xml_values_output: str = "values.xml", xml_definitions_output: str = "definitions.xml",
            arff: bool = False, csv: bool = False, window_length: int = None, window_overlap_fraction: float = None):
        """Run the current configuration
        Added parameters will overwrite the configuration"""
        command = f"java -Xmx{self.ram}g" \
                  f' -jar "jSymbolic2.jar" ' \
                  f"{'-arff ' if arff else ''}" \
                  f"{'-csv ' if csv else ''}" \
                  f'"{path}" "{xml_values_output}" "{xml_definitions_output}" ' \
                  f"{window_length if window_length else ''} {window_overlap_fraction if (window_length and window_overlap_fraction) else ''}"

        with cd(self.working_dir.as_posix()):
            logging.info("Executing:", command)
            process = subprocess.run(shlex.split(command),
                                     stdout=subprocess.PIPE,
                                     universal_newlines=True)
            logging.info(process.stdout)

    def create_config(self, path: str, xml_values_output: str = "values.xml", xml_definitions_output: str = "definitions.xml",
                      arff: bool = False, csv: bool = False, window_length: int = None, window_overlap_fraction: float = None):

        config = f"""
        <output_files>
            feature_values_save_path={xml_values_output}
            feature_definitions_save_path={xml_definitions_output}
        <input_files>
            {path}
            """






