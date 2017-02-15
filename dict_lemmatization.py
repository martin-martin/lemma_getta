# coding: utf-8
import os
import csv
from pprint import pformat
from collections import OrderedDict


#################### PREPARATIONS ####################

#================ NECESSARY: SPECIFY LANGUAGE! ================#

language = "de" # en = English, es = Spanish, de = German
filename = "full_freq.csv"

#==============================================================#


# for debugging - use the function to see whether the dicts have senseful entries
def peek(dictionary, n):
    """returns n random entries of a dictionary for inspection."""
    return {k: dictionary[k] for k in list(dictionary.keys())[:n]}

# this should be able to stay the same for all files, change to process sliced files
word_freq_file = "source/words/{0}_{1}".format(language, filename)

# get the data from the files
with open(word_freq_file, "r") as f:
    reader = csv.reader(f)
    freq = {rows[1]:rows[2] for rows in reader}

with open("lemmatize/{0}/lemmatization-{0}.tsv".format(language, language), "r") as f:
    reader = csv.reader(f, delimiter="\t")
    lemmas = {rows[1]:rows[0] for rows in reader}

# remove the header from the frequency file
del freq["word"]


#################### PROCESSING ####################

new = dict()

for w, f in freq.items():
    # if the word is an inflection in the lemma dict
    if w in lemmas.keys():
        # get its lemma form
        lem = lemmas[w]
        # if the lemma is already in the new dict
        if lem in new.keys():
            # appends new dict entry to the dict
            # mapping the inflection to its frequency
            new[lem].update({w: int(f)})
        # otherwise create a new entry
        else:
            new[lem] = {w: int(f)}
    # if there is no lemma mapping present
    else:
        # treat the original word as a lemma and add to dict
        no_lem = w
        new[no_lem] = {w: int(f)}


freq_dict = dict()

for k, v in new.items():
    # adding all the separate inflection frequencies
    lem_freq = sum(f for f in new[k].values())
    freq_dict[k] = (lem_freq, new[k])


#################### OUTPUT ####################

# sorting the results descending
ordered_freq = OrderedDict(sorted(freq_dict.items(), key=lambda f: f[1][0], reverse=True))

# create the output folder
if not os.path.exists("lemma_output/{0}".format(language)):
    os.makedirs("lemma_output/{0}".format(language))

# write the frequency text file
with open("lemma_output/{0}/{1}_lemma_freq.txt".format(language, language), "w") as f:
    f.write("## Lemma-frequencies for: {0}. Number of lemmas: {1} ##".format(language, len(ordered_freq)))
    f.write(pformat(ordered_freq))