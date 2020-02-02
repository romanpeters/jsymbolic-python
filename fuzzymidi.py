import csv
import pandas as pd

import ntpath
from pathlib import Path

from jsymbolic import FileItem
from pprint import pprint

from fuzzywuzzy import fuzz
from tqdm import tqdm

def checkmapping():

    mapping = pd.read_csv(
        filepath_or_buffer="MIDItoYEAR.csv",sep=",",index_col=0,header=0,quoting=csv.QUOTE_ALL,encoding="utf-8"
    )

    mapping["MIDI_query"] = mapping["MIDI"].apply(
        lambda x: FileItem.flatten(x.split('/')[0]) + "-" +FileItem.flatten(x.split('/')[1].replace('.mid',''))
    )
    return mapping

#start code based on work by peer SMT team A. Saadon and S. Galanakis
def string_cut(var):
    if ' -' in var:
        return var.index(' -')
    else:
        return -1
  
def find_best_file(query,files):

    best_distance = -1
    best_title = ""

    for midi_file in files:
        distance = fuzz.ratio(midi_file,query)
        if distance > best_distance:
            best_distance = distance
            best_title = midi_file
    return best_title,best_distance

#end code based on work by peer SMT team A. Saadon and S. Galanakis

def get_files(mapping): 
    
    files = list(map(lambda x: x.name, list(Path("/Users/romanpeters/Desktop/SMT_Project/RAG-private/RAG/run").rglob('*.mid'))))
    
    mapping["match_found"] = [""] * len(mapping)
    mapping["match_score"] = [0] * len(mapping)

    for index,mep in tqdm(mapping.iterrows(), total=len(mapping)):
        #print(f'Checking if {mep["MIDI_query"]} exists..')
        best_title, best_distance = find_best_file(mep["MIDI_query"],files)
        #print(f'resultaat: {best_title} met score {best_distance}')
        mapping.at[index, 'match_found'] = best_title
        mapping.at[index, 'match_score'] = best_distance

    mapping.to_csv(path_or_buf="combined_mapping.csv",header=True,index=True)
    print("Written results of fuzzy matching mapping to ./combined_mapping.csv")

mapping = checkmapping()

get_files(mapping)
