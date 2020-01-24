import sys as sys
import pandas as pd
import matplotlib.pyplot as plt
from fuzzywuzzy import fuzz
from pathlib import Path

#Find all titles for which there is a solid year and for which we have a midi file in our compendium.

#input compendium and subset
full_compendium = pd.read_csv('Compendium.csv')
full_subset = pd.read_csv('subset.csv')

#clean compendium for missing/bad years
yeared_compendium = full_compendium[full_compendium.Year.str.len() == 4]
#clean compendium for unavailable midi's
yeared_compendium = yeared_compendium[~yeared_compendium.Midi.isna()]
#make compendium titles lower case
yeared_compendium['Title'] = yeared_compendium['Title'].str.lower()

def string_cut(var):
    if ' -' in var:
        return var.index(' -')
    else:
        return -1

#get a list of all the names of all the midi files in our working folder
midi_paths = list(Path().rglob('*.mid'))
raw_midi_paths = list(map(lambda x: x.name, midi_paths)) #get raw path string
filtered_midi_names = [x[0:-4] for x in raw_midi_paths] #through away the extention
midi_titles = list(map(lambda x: x[0: string_cut(x)], filtered_midi_names)) #get only the titles of the midi's and remove contrib
midi_titles = [x.lower() for x in midi_titles] #lower case the titles
midi_copy = midi_titles.copy() #make a copy

#Find best matching song in the available ones.
def find_best(st):
    best_title = ''
    best_distance = 0
    for title in midi_copy:
        distance = fuzz.ratio(st, title)
        if distance > best_distance:
            best_distance = distance
            best_title = title
    return best_distance, best_title

#Create csv with extra column that contains the path.
for index, row in yeared_compendium.iterrows():
    if index%100 == 0: print(index)
    #if index ==100: break
    best_distance, best_title = find_best(row['Title']) #for each compendium title find the best midi that matches it closest
        
    if best_distance > 80: #if distance between the compendium title and midi is close enough
        midi_copy.remove(best_title) #make midi unavailable for a next assignment
        index2 = midi_titles.index(best_title)
        yeared_compendium.at[index, 'File'] = midi_paths[index2] #and assign midi to current one


yeared_compendium = yeared_compendium[~yeared_compendium.File.isna()] #remove the titles for which we did not find a midi
comp = yeared_compendium.drop_duplicates(subset=['File'], keep=False) #drop titles that have a midi file that is used by more than one title
comp.to_csv('Pathed_withoutduplicates.csv', encoding='utf-8', index=False) #save this subset

print('done')




