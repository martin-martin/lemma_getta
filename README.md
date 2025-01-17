# Baseword Frequency Lists
Generating an ordered list of baswords, descending by frequency. The source files are:

1. **absolute word counts** generated from freely available open corpora, with a focus on spoken language
2. **basewords** generated from a lemmatization list generated through API calling those words to receive their basewords

It is necessary to specify the language. If the data is available for the specified language, the code outputs an (unordered) JSON file with the basewords and their absolute frequency counts (these are constituted by the sum of all frequencies of their associated inflections). Further it outputs an ordered CSV file, starting with the most frequent word in the language, then descending from there.

## Note
The word data is to a large degree composed of user-generated movie subtitle data. Thus, especially for low-frequency words (= towards the end of the list), there are many words that might not even be part of the specified language. However, due to the large corpus size, the high-frequency words should be (hopefully) representative of a more oral use of the language. This holds many caveats, of course, so take care when consuming the data. Feedback is welcome : )
