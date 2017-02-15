# coding: utf-8
import csv
from collections import OrderedDict, Counter
from pprint import pformat

##################### WORK HERE, DEAR USER #####################

# specify language
language = "es"
# specify file to process:
word_freq_file = "source/words/{0}_full_freq.csv".format(language)

################################################################

# useful function for data peeking
def peek(dictionary, n):
    """returns n random entries of a dictionary for inspection."""
    return {k: dictionary[k] for k in list(dictionary.keys())[:n]}

#========= FETCHING AND CLEANING THE DATA
with open(word_freq_file, "r") as f:
    reader = csv.reader(f)
    freq = {rows[1]:rows[2] for rows in reader}

with open("source/lemmas/{0}_lemPOS.csv".format(language), "r") as f:
    reader = csv.reader(f)
    lemmas = {rows[2]:rows[1] for rows in reader}

# remove the headers
del freq["word"]

#========= WEAVING IT TOGETHER
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


#========= ADDING EXTRA INFO
freq_dict = dict()

for k, v in new.items():
    # adding all the separate inflection frequencies
    lem_freq = sum(f for f in new[k].values())
    freq_dict[k] = (lem_freq, new[k])


#========= PUTTING THINGS IN ORDER
ordered_freq = OrderedDict(sorted(freq_dict.items(), key=lambda f: f[1][0], reverse=True))


#========= A NEW FILE IS BORN
with open("sink/{0}_lemma_freq.txt".format(language), "w") as f:
    f.write(pformat(ordered_freq))

# for those who are curious
#len(ordered_freq)