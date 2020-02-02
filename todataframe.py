import sys
import os
import logging
import random
import csv
import numpy as np
import pandas as pd
import ntpath
import re
from random import seed

mapping = None

def read_midi_mapping():

	mapping = pd.read_csv("combined_mapping.csv")
	mapping.columns = ["id","midi_unformatted","year","midi_query","midi","match_score"]
	return mapping
	
def read_csv_from_folder(folder,mapping):
	
	midi_names = []
	datasets = []
	
	# get midi files
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
	
	for filename in filenames:
		result = read_csv_file(filename,midi_names,datasets)
		midi_names = result[0]
		datasets = result[1]
		columns = result[2]

	seed(1)

	df1 = pd.DataFrame(datasets) 
	print("Creating dataframe..")
	
	columns.pop(0) # remove index column
	df1.columns = columns
	df1.insert(0,"midi",midi_names)
	
	# print("Losse stukken:")
	# print(df1)
	# print(mapping)

	df = pd.merge(df1, mapping, on='midi')
	print(f'After merging there are {len(df)} rows in df')
	df.to_csv(path_or_buf="dataframe.csv",header=True,index=True)
	print("Written merges to dataframe.csv file succesfully")


def read_csv_file(filename,midi_names,datasets):
	columns = []
	with open(filename) as File:  
		print(f'Reading csv: {filename}')
		reader = csv.reader(File,delimiter=',')

		row_count = 0
		for row in reader:
			if row_count == 0:
				# print(f'Column names are {", ".join(row)}')
				col_count = len(row)
				columns = row

				row_count += 1
			else:
				midi_name = '-'.join(ntpath.basename(row[0]).split('-')[1:])
				midi_names.append(midi_name)

				row.pop(0)

				datasets.append(np.array(row, dtype='<U10')) ## todo: set dtype properly
				row_count += 1

		row_count -= 1 # for the column name row
		print(f'There are {col_count} columns')
		print(f'There are {row_count} rows')
		return midi_names,datasets,columns



mapping = read_midi_mapping()
read_csv_from_folder("/Users/romanpeters/Desktop/SMT_Project/RAG-private/RAG/run",mapping)
# change this to match your local folder
