# jsymbolic-python
Python interface for jSymbolic 2

## Example code

Python code:
```
import jsymbolic

jsym = jsymbolic.App("/path/to/jSymbolic2.jar")

# use a custom config file
jsym.set_config("/path/to/config.txt"))

# show the current config file
print(jsym.get_config())

# analyse a MIDI file or a collection of MIDI files
jsym.run("/path/to/dir/or/file.midi", xml_values_output="values.xml", xml_definitions_output="definitions.xml", csv=True)
```


