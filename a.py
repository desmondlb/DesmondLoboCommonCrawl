import gzip
import io
from code_1 import Extractor
import requests


base_url = 'https://data.commoncrawl.org/'

file_ids = [('2020', '24')]

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
    if len(res) > 1000: break
    file_url = base_url + f'crawl-data/CC-MAIN-{i1}-{i2}/warc.paths.gz'

    uri_list = get_uri_list(file_url)
    for file_uri in uri_list:
        if len(res) > 1000: break
        hits, matches, entries, match_set, non_parsed = extractor.iterator(url=base_url + file_uri)

        if non_parsed: np.append(base_url + file_uri)
        if matches:
            res.update(match_set)


print(res)
print(np)