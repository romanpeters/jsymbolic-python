# fuzzymidi.py
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
    
    # print(mapping)
    
    return mapping


    #courtesy of 
def string_cut(var):
    if ' -' in var:
        return var.index(' -')
    else:
        return -1
  
def find_best_file(query,files):

    best_distance = -1
    best_title = ""

    for midi_file in files:
        # distance = 0
        distance = fuzz.ratio(midi_file,query)
        if distance > best_distance:
#            print(f'best_title {midi_file} is better')
            best_distance = distance
            best_title = midi_file
    return best_title,best_distance


def get_files(mepje): 
    
    files = list(map(lambda x: x.name, list(Path("/Users/romanpeters/Desktop/SMT_Project/RAG-private/RAG/run").rglob('*.mid'))))
    # pprint(files)
    mepje["match_found"] = [""] * len(mepje)
    mepje["match_score"] = [0] * len(mepje)

    for index,mep in tqdm(mepje.iterrows(), total=len(mepje)):
#        print(f'Checking if {mep["MIDI_query"]} exists..')
        best_title, best_distance = find_best_file(mep["MIDI_query"],files)
#        print(f'resultaat: {best_title} met score {best_distance}')
        mepje.at[index, 'match_found'] = best_title
        mepje.at[index, 'match_score'] = best_distance

        # mepje["ID"==index,"match_found"] = best_title    
        # mepje["ID"==index,"match_score"] = best_distance    
            # print(f'Result when comparing {midi_file}: {distance}')
    # pprint(mepje)
    mepje.to_csv(path_or_buf="combined_mapping.csv",header=True,index=True)

    # filtered_midi_names = [x[0:-4] for x in raw_midi_paths] #through away the extention
    # midi_titles = list(map(lambda x: x[0: string_cut(x)], filtered_midi_names)) #get only the titles of the midi's and remove contrib
    # # pprint(midi_titles)
    # midi_titles = [x.lower() for x in midi_titles] #lower case the titles
    # midi_copy = midi_titles.copy() #make a copy




mepje = checkmapping()

get_files(mepje)
