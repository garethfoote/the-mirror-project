import json
import ctypes
from pprint import pprint
json_data=open('flanagan.json')

data = json.load(json_data)
reduced_data = dict()
max = 20
for key in data:
    count = 0
    for item in data[key]:
        count = count+1
        if count <= max:
            if key not in reduced_data:
                reduced_data[str(key)] = dict()
            reduced_data[key][item] = data[key][item]

print json.dumps(reduced_data);
