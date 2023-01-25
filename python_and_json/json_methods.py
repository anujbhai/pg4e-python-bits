import json
import xml.etree.ElementTree as ET

# json.dumps()
# -------------------------------------------------
# takes a python object and serializes it into JSON
# -------------------------------------------------
data1 = {}
data1['name'] = 'Chuck'
data1['phone'] = {}
data1['phone']['type'] = 'intl'
data1['phone']['number'] = '+1 734 303 4456'
data1['email'] = {}
data1['email']['hide'] = 'yes'

# Serialize
print(json.dumps(data1, indent=4))

# json.loads()
# -------------------------------------------------
# takes a string containing valid JSON
# and deserializes it into python dictionary
# or list as appropriate
# -------------------------------------------------
data2 = '''
{
    "name": "Chuck",
    "phone": {
        "type": "intl",
        "number": "+1 734 303 4456"
    },
    "email": {
        "hide": "yes"
    }
}
'''

info = json.loads(data2)
print("Name: ", info["name"])
print("Phone: ", info["phone"]["number"])

# json.dumps() with list
# ----------------------
data3 = []
data3_entry = {}

data3_entry['id'] = '001'
data3_entry['x'] = '2'
data3_entry['name'] = 'Chuck'
data3.append(data3_entry)

data3_entry = {}

data3_entry['id'] = '009'
data3_entry['x'] = '7'
data3_entry['name'] = 'Brent'
data3.append(data3_entry)

print(json.dumps(data3, indent=4))

# json.loads() with list
# ----------------------
data4 = '''
[
    {
        "id": "001",
        "x": "2",
        "name": "Chuck"
    },
    {
        "id": "009",
        "x": "7",
        "name": "Brent"
    }
]
'''

info = json.loads(data4)
print('User count: ', len(info))

for item in info:
    print('Name', item['name'])
    print('Id', item['id'])
    print('X', item['x'])

# find() method for serializing/deserializing 'xml'
# -------------------------------------------------
data5 = '''
<person>
    <name>Chuck</name>
    <phone type="intl">+1 734 303 4456</phone>
    <email hide="yes" />
</person>
'''

tree = ET.fromstring(data5)
print('Name: ', tree.find('name').text)
print('Attr: ', tree.find('email').get('hide'))
