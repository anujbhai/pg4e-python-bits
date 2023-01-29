from elasticsearch import Elasticsearch
from elasticsearch import RequestsHttpConnection
import time
import copy
import json
import hashlib
import hidden

bookfile = input("Enter book file (i.e. pg14091.txt): ")

if bookfile == "" : bookfile = "pg14091.txt"

indexname = bookfile.split('.')[0]

fhand = open(bookfile)

secrets = hidden.elastic()

es = Elasticsearch(
    [secrets['host']],
    http_auth=(secrets['user'], secrets['pass']),
    url_prefix=secrets['prefix'],
    scheme=secrets['scheme'],
    port=secrets['port'],
    connection_class=RequestsHttpConnection,
)
indexname = secrets['user']

res = es.indices.delete(index=indexname, ignore=[400, 404])

print("Dropped index", indexname)
print(res)

res = es.indices.create(index=indexname)

print("Created the index...")
print(res)

para = ''
chars = 0
count = 0
pcount = 0

for line in fhand:
    count = count + 1
    line = line.strip()
    chars = chars + len(line)

    if line == "" and para == "" : continue

    if line == "":
        pcount = pcount + 1
        doc = {
            "offset": pcount,
            "content": para
        }

        m = hashlib.sha256()
        m.update(json.dumps(doc).encode())
        pkey = m.hexdigest()

        res = es.index(index=indexname, id=pkey, body=doc)

        print("Added document", pkey)

        if pcount % 100 == 0:
            print(pcount, "loaded...")
            time.sleep(1)

        para = ''
        continue

    para = para + " " + line

res = es.indices.refresh(index=indexname)
print("Index refreshed", indexname)
print(res)

print(" ")
print("Loaded", pcount, "paragraphs", count, "lines", chars, "characters")
