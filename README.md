# DesmondLoboCommonCrawl

## Approach

In this we first get the WARC paths file for the given month. This file further contains a list of .gz compressed files, each of which has a list of urls.
So I first wrote a parser for this which outputs a string containing the .gz file path
Then for each url found we append a base path "https://data.commoncrawl.org/" and call the iterator methof from the object of the Extractor Class to process all the URLs present in the file.

The iterator in turn calls the matcher function which matches the contents of the web page to a corpus I created that contains a list of words that is used to mark a web page if it's related to the topic of economic impact of covid.

The corpus is an essentially a python dictionary that contains two sets of words. One for covid related words and one for economics related words that relate to the global/national economies.

To make the search more better I use the NLTK library to remove the stopwords and then search whether the required words are present in the remaining text data.

Following were the challenges I faces.

###Challenge: 
Creating the appropriate corpus containing the relevant words to search, and writitng a function that gives a clean output of the html page (Using Beautifulsoup).

###Failed approach. 
Initially I tried to use a fuzzy text matching library called "fuzzywuzzy" which can be used to detect string similarity. However, in the end I resorted to just checking if a word is present in the corpus. This was because fuzzywuzzy would take O(n) time each time to get the higest scoring matches.

###Assumptions:
One key assumption that I used to reduce the search space is that if we go through 80% of the html page content and still not find anything we can just assume that the page is not related to the topic.

