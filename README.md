# jsymbolic-python
Python interface for jSymbolic 2

## Example code

Python code:
```
import jsymbolic

# Optionally adjust the log level
import logging
logging.getLogger().setLevel(logging.CRITICAL)

DIR_PATH = "/path/to/some/output/dir"

# Run the preprocessor to rename the MIDI files and copy them to DIR_PATH.
# Without preprocessing, jSymbolic might fail if special characters are used in the file names.
preprocessor = jsymbolic.PreProcessor(input_path="/path/to/dir/or/file.midi", output_path=DIR_PATH)
preprocessor.run()

# The App class is used to control jSymbolic.
jsym = jsymbolic.App("/path/to/jSymbolic2.jar")

# Using per_file creates an XML file for each MIDI file. 
# This prevents jSymbolic from running out of memory on large datasets
# and allows for partial runs. 
jsym.run(path=DIR_PATH, per_file=True, skip_processed=True)
```

## Dependencies
Optionally install tqdm for a progress bar when using `per_file=True`.  
```pip install tqdm```


