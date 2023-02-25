from warcio.archiveiterator import ArchiveIterator
import re
import requests
import sys
from config import KEY_PHRASES, THRESHOLD
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import nltk
import string

nltk.download('stopwords')


class Extractor():
    def __init__(self):

        self.regex = re.compile(r'\bECONOMIC\b', re.IGNORECASE)
        self.entries = 0
        self.matching_entries = 0
        self.hits = 0
        self.matches = set()
        self.not_parsed = False
        self.covid_words = set(map(lambda x: x.lower(), KEY_PHRASES["covid"]))
        self.economics_words = set(map(lambda x: x.lower(), KEY_PHRASES["economics"]))
        self.c_words = set()
        self.e_words = set()
        self.stop_words=set(stopwords.words('english'))


    def pre_process_content(self, page_content):
        soup = BeautifulSoup(page_content, "html.parser")
        for data in soup(['style','script']):
            data.decompose()
        
        return ' '.join(soup.stripped_strings)
        

    def matcher(self, page_content):
        strOutput = self.pre_process_content(page_content)
        text  = str(strOutput.encode('utf-8'))

        finalTokens=[]
        word_list = strOutput.strip().lower().translate(str.maketrans('', '', string.punctuation)).split(" ")
        for word in word_list:
            if word not in self.stop_words:
                finalTokens.append(word)

        for i, word in enumerate(finalTokens):
            if (len(self.c_words) >= 2 and len(self.e_words) >= 2) or i > THRESHOLD*len(page_content): break
            if word in self.covid_words: self.c_words.add(word)
            if word in self.economics_words: self.e_words.add(word)

    
    def iterator(self, url = None):
        file_name = url

        if len(sys.argv) > 1:
            file_name = sys.argv[1]

        stream = None
        if file_name.startswith("http://") or file_name.startswith("https://"):
            stream = requests.get(file_name, stream=True).raw
        else:
            stream = open(file_name, 'rb')
        try:
            for record in ArchiveIterator(stream):
                if record.rec_type == "warcinfo":
                    continue

                if not ".com/" in record.rec_headers.get_header("WARC-Target-URI"):
                    continue

                self.entries += 1
                contents = (
                    record.content_stream()
                    .read()
                    .decode("utf-8", "replace")
                )
                # m = self.regex.search(contents)
                self.matcher(contents)

                if len(self.c_words) >= 2 and len(self.e_words) >= 2:
                    self.matching_entries = 1
                    # self.hits += 1
                    self.matches.add(record.rec_headers.get_header("WARC-Target-URI"))
                    m = self.regex.search(contents, m.end())
                self.c_words.clear()
                self.e_words.clear()

                # while m:
                #     m = self.regex.search(contents, m.end())
                #     self.hits += 1
        except Exception as e:
            self.not_parsed = True

        finally:
            return self.hits, self.matching_entries, self.entries, self.matches, self.not_parsed
    
if __name__ == "__main__":
    obj = Extractor()
    hits, matches, entries, match_set = obj.iterator(url="https://data.commoncrawl.org/crawl-data/CC-MAIN-2020-05/segments/1579250589560.16/warc/CC-MAIN-20200117123339-20200117151339-00011.warc.gz")

    print(hits)
    