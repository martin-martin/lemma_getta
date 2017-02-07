import ast
import pandas as pd

# read generated frequency file
# this detour is taken because something doesnt work with JSON load()
with open("word_frequency.json") as f:
	wf = f.read()
# translating back to a dict
word_freq = ast.literal_eval(wf)

#specify thee slice of the frequencies to keep
start_slice = 0
end_slice = -1

# sort the dict values according to frequency and keep the specified slice
fdf = pd.DataFrame(list(word_freq.items()), columns=["word", "frequency"])
sorted_fdf = fdf.sort_values(by=["frequency"], ascending=[False])
sliced_fdf = sorted_fdf[start_slice:end_slice]

# create a new file with the sliced values
sliced_fdf.to_csv("../lemmatize/freq_{0}_{1}.csv".format(start_slice, end_slice), encoding="utf-8")