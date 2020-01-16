# jsymbolic-python
Python interface for jSymbolic 2

## Example code
```
import jsymbolic

jsym = jsymbolic.App("/path/to/jSymbolic2.jar")

# analyse a MIDI file or a collection of MIDI files
jsym.run("/path/to/dir/or/file.midi", xml_values_output="values.xml", xml_definitions_output="definitions.xml", csv=True)

# You can also create a config file first, which extends jSymbolicDefaultConfigs.txt
jsym.create_config("/path/to/dir/or/file.midi", config_output="config.txt")

jsym.run_config("config.txt")
```
