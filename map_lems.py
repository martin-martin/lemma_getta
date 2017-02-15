# coding: utf-8

# # Baseword Frequency Lists
# Generating an ordered list of baswords, descending by frequency.
# The source files are:
#
# 1. **absolute word counts** generated from freely available open corpora,
#    with a focus on spoken language
# 2. **basewords** generated from a lemmatization list proofread with API calls
#
# It is necessary to specify the language. If the data is available
# for the specified language, the code outputs an (unordered) JSON file
# with the basewords and their absolute frequency counts (these are constituted
# by the sum of all frequencies of their associated inflections).
# Further it outputs an ordered CSV file, starting with the most frequent word
# in the language, then descends.
#
# ## Note
# The word data is to a large degree composed of user generated subtitle data.
# Thus, especially towards the end of the list, there are many words that might
# not even be part of the specified language. However, due to the large
# corpus size, the high-frequency words should be (hopefully) representative
# of a more oral usage of the language. Many caveats, of course, so take care
# when consuming the data. Feedback is welcome : )



################# Part 1 - Reading data and gathering input

import csv
import pandas as pd
from collections import OrderedDict, Counter

# Change the language data to process for a different file
# (currently: English (`"en"`), Spanish (`"es"`) and French (`"fr"`))

####################################################################
################# specify language #################
language = "fr"
################# specify file to process #################
word_freq_file = "source/words/{0}_full_freq.csv".format(language)
####################################################################

# read in the word frequency data
with open(word_freq_file, "r") as f:
    reader = csv.reader(f)
    freq = {rows[1]:rows[2] for rows in reader}
# read in the word baseword mappings
with open("source/lemmas/{0}_lemPOS.csv".format(language), "r") as f:
    reader = csv.reader(f)
    lemmas = {rows[2]:rows[1] for rows in reader}
# remove the headers
del freq["word"]

def peek(dictionary, n):
    """returns n random entries of a dictionary for inspection."""
    return {k: dictionary[k] for k in list(dictionary.keys())[:n]}


################# Part 2 - Weaving the data into one

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

# generating an additional count for the sum of all inflections
freq_dict = dict()
for k, v in new.items():
    # adding all the separate inflection frequencies
    lem_freq = sum(f for f in new[k].values())
    freq_dict[k] = (lem_freq, new[k])


################# Part 3 - Output

# Extract only a part of the data
# Currently we only need the baseword and its frequency in a easily readable file format.
bw_freq = {k:v[0] for k, v in freq_dict.items()}

# export the JSON file
with open("sink/{0}_bw_freq.json".format(language), "w") as f:
    json.dump(bw_freq, f, ensure_ascii=False)

# ## Put that in order, please!
# Creating an ordered CSV file, for even easier processing.
lem_freq_ord = sorted(bw_freq.items(), key=lambda f: f[1], reverse=True)

# removing a '*'' mapping from the spanish entries
if language == "es":
    lem_freq_ord.pop(18)

# PEEK HERE TO SEE WHETHER IT'S ALL RIGHT!
#print(lem_freq_ord)

# create a df and export it to CSV
df = pd.DataFrame(lem_freq_ord, columns=["baseword", "frequency"])
df.to_csv("sink/{0}_bw_freq.csv".format(language))