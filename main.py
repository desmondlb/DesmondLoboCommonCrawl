import gzip
import io
from extractor import Extractor
import requests


base_url = 'https://data.commoncrawl.org/'

file_ids = [('May/June', '24'), ('July', '29'), ('March/April', '16')]

extractor = Extractor()

def get_uri_list(file_url):
    res = requests.get(file_url, stream=True).raw
    res_content = res.read()
    stream = io.BytesIO(res_content)
    decompressor = gzip.GzipFile(fileobj=stream, mode='r')
    chunk = 1
    accumulator = ''
    while chunk:
        chunk = decompressor.read(8192)
        accumulator += chunk.decode('utf-8')
    decompressor.close()
    return accumulator.split('\n')

res = set()
np = []
for (i1, i2) in file_ids:
    file_url = base_url + f'crawl-data/CC-MAIN-2020-{i2}/warc.paths.gz'

    uri_list = get_uri_list(file_url)
    for file_uri in uri_list:
        if len(res) > 1000: break
        extractor.matches.clear()
        match_set, non_parsed = extractor.iterator(url=base_url + file_uri)

        if non_parsed: np.append(base_url + file_uri)
        if match_set:
            res.update(match_set)
            print(match_set)
            with open("output.txt", "w+") as f:
                f.write("\n".join(match_set) + " Months: " + i1)
                f.flush
