import jsymbolic

jsym = jsymbolic.App("/Users/romanpeters/Desktop/jsymbolic_cli/jSymbolic2.jar")

# analyse a MIDI file or a collection of MIDI files
jsym.run("/Users/romanpeters/Desktop/SMT_Project/RAG-private/RAG/MathewCollection/Cookie Jar, Melody Lane & Crider/Alexander's Ragtime Band - Melody Lane.mid", xml_values_output="/Users/romanpeters/Desktop/SMT_Project/values.xml", xml_definitions_output="/Users/romanpeters/Desktop/SMT_Project/definitions.xml", csv=True)

# You can also create a config file first, which extends jSymbolicDefaultConfigs.txt
jsym.create_config("/path/to/dir/or/file.midi", config_output="config.txt")

#jsym.run_config("config.txt")