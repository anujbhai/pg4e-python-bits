import xml.etree.ElementTree as ET
import json

file_name = input('Enter file name: ')

if (len(file_name) < 1) : file_name = 'Library.xml'

def look_up(d, key):
    found = False

    for child in d:
        if found : return child.text
        if child.tag == 'key' and child.text == key:
            found = True

    return None

stuff = ET.parse(file_name)
all = stuff.findall('dict/dict/dict')
print('Dict count: ', len(all))

json_file = open('library.jstext', 'w', newline='')

for entry in all:
    if (look_up(entry, 'Track ID') is None) : continue

    name = look_up(entry, 'Name')
    artist = look_up(entry, 'Artist')
    album = look_up(entry, 'Album')
    count = look_up(entry, 'Play Count')
    rating = look_up(entry, 'Rating')
    length = look_up(entry, 'Total Time')

    if name is None or artist is None or album is None:
        continue

    if length is None : length = 0
    if count is None : count = 0
    if rating is None : rating = 0

    entry = {'name': name, 'artist': artist, 'album': album, 'count': int(count), 'rating': int(rating), 'length': int(length)}

    # Don't indent - we want this to be all one line
    json_file.write(json.dumps(entry))
    json_file.write('\n')

print("Results are in library.jstext")
json_file.close()
