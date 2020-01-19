import sys
import os
import logging

# todataframe.py
import csv
import numpy as np
import pandas as pd
import glob

# todo: add path to read filenames from as a parmeter.

def read_csv_from_folder(folder):
	
	midi_names = []
	datasets = []
	

	# get midi files
	# todo: get them from a folder or csv file automatically
	if not folder: # use current working directory
		folder = os.getcwd()
	
	print(f'folder: {folder}')		
	filenames =[]
	for file in os.listdir(folder):
		print(file)
		if file.endswith(".csv"):
			print(os.path.join(folder, file))
			filenames.append(os.path.join(folder, file))
	
	print(filenames)
	
	# fallback
	# filenames = ['examples/values.csv','examples/values.csv']

	for filename in filenames:
		# print(filename)
		result = read_csv_file(filename,midi_names,datasets)
		midi_names = result[0]
		datasets = result[1]

	print(f'Midi names and datasets:')
	print(midi_names)
	print(datasets)

	# todo: concat this into a matrix/dataframe
	df = pd.DataFrame(datasets) 
	print(df)


def read_csv_file(filename,midi_names,datasets):
	with open(filename) as File:  
		print(f'Reading csv: {filename}')
		reader = csv.reader(File,delimiter=',')

		row_count = 0
		for row in reader:
			# print(row_count)
			# print(row)
			# column names
			if row_count == 0:
				# print(f'Column names are {", ".join(row)}')
				col_count = len(row)
				

				row_count += 1
			else:
				midi_name = row[0]
				midi_names.append(midi_name)
				# print(midi_name)
				row.pop(0)
				datasets.append(np.array(row, dtype='<U10')) ## todo: set dtype properly
				row_count += 1

		row_count -= 1 # for the column name row
		print(f'There are {col_count} columns')
		print(f'There are {row_count} rows')
		return midi_names,datasets


read_csv_from_folder("examples")


# todo: fucntion to extract all column names, they are the first row in any csv file from Jsymbolic