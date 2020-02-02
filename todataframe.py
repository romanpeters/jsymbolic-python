import sys
import os
import logging
import random
# from random import seed
# from random import random
# seed random number generator

import csv
import numpy as np
import pandas as pd
# todo: requirements 
# todo: add path to read filenames from as a parmeter.
import ntpath
import re

from random import seed







# mapping = pd.DataFrame ({'id':  [],'midi': [],'year': []}, columns = ['id','midi','year'])
mapping = None

def read_midi_mapping():

	mapping = pd.read_csv("combined_mapping.csv")
	mapping.columns = ["id","midi_unformatted","year","midi_query","midi","match_score"]
	
	mapping.to_csv(path_or_buf="mapping.csv",header=True,index=True)
	return mapping
	# print(mapping)


def read_csv_from_folder(folder,mapping):
	
	midi_names = []
	datasets = []
	

	# get midi files
	# todo: get them from a folder or csv file automatically
	if not folder: # use current working directory
		folder = os.getcwd()
	
	print(f'folder: {folder}')		
	filenames =[]
	for file in os.listdir(folder):
		if file.endswith(".csv"):
			print(f"Found CSV: {file}")
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
		columns = result[2]

	# print(f'Midi names and datasets:')
	# print(midi_names)
	# print(datasets)
	# columns.pop()
	# todo: concat this into a matrix/dataframe
	seed(1)

	df1 = pd.DataFrame(datasets) 
	print("Creating dataframe..")
	# print(df1.columns)
	columns.pop(0)
	df1.columns = columns
	rand_years = [random.randrange(1901, 2000) for iter in range(len(midi_names))]
	# print(rand_years)
	# df1.insert(0,"year",rand_years)
	df1.insert(0,"midi",midi_names)
	# print(columns)
	print("Losse stukken:")
	print(df1)
	print(mapping)

	df = pd.merge(df1, mapping, on='midi')
	print(f'After merging there are {len(df)} rows in df')
	df.to_csv(path_or_buf="dataframe.csv",header=True,index=True)
	print("./Written to dataframe.csv file")


def read_csv_file(filename,midi_names,datasets):
	columns = []
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
				columns = row

				row_count += 1
			else:
				midi_name = '-'.join(ntpath.basename(row[0]).split('-')[1:])
				midi_names.append(midi_name)

				# print(midi_name)
				# row[0] = midi_name
				row.pop(0)
				# print(row)
				datasets.append(np.array(row, dtype='<U10')) ## todo: set dtype properly
				row_count += 1

		row_count -= 1 # for the column name row
		print(f'There are {col_count} columns')
		print(f'There are {row_count} rows')
		return midi_names,datasets,columns



mapping = read_midi_mapping()
read_csv_from_folder("/Users/romanpeters/Desktop/SMT_Project/RAG-private/RAG/run",mapping)

# todo: fucntion to extract all column names, they are the first row in any csv file from Jsymbolic
