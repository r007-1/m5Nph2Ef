import json
import pandas
import io

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches


def locations_of_substring(string, substring):
    """Return a list of locations of a substring."""
    substring_length = len(substring)
    def recurse(locations_found, start):
        location = string.find(substring, start)
        if location != -1:
            return recurse(locations_found + [location], location+substring_length)
        else:
            return locations_found
    return recurse([], 0)


def clean(filename):
    with open(filename) as file:
        lines = file.readlines()
    try:
        json.loads(lines[-1])
    except ValueError:
        edit = lines[-2]
        edit = edit[:-2]
        lines[-2] = edit + "]"
        lines = lines[:-1]
    with open(filename.replace('.json', '-clean.json'), 'w') as file:
        file.write(''.join(lines))


def merge(filenames, outputFilename):
    c = list()
    for i in range(0, len(filenames)):
        with open(filenames[i]) as file:
            lines = file.readlines()
            if (i != len(filenames) - 1):
                lines[-1] = lines[-1].replace("}]","},\n")
            if (i != 0):
                lines[0] = lines[0].replace("[{", "{")
            for i in range(0, len(lines)):
                c.append(lines[i])
    with open(outputFilename, 'w') as file:
        file.write(''.join(c))


### Format ASOS products
def tidy_asos_us(filename):
    items = pandas.read_json(filename)
    i = items
    i['date_added'] = i['date_added'].apply(lambda x: x[0])
    i['date_last_updated'] = i['date_last_updated'].apply(lambda x: x[0])
    i['currency'] = i['currency'].apply(lambda x: x[0:3])

i = p
i['imglink_1'] = i['imglink_1'].apply(lambda x: re.sub("\?\$(.*)","", x))
i['imglink_2'] = i['imglink_2'].apply(lambda x: re.sub("\?\$(.*)","", x))
i['imglink_3'] = i['imglink_3'].apply(lambda x: re.sub("\?\$(.*)","", x))
i['imglink_4'] = i['imglink_4'].apply(lambda x: re.sub("\?\$(.*)","", x))
p = i
    i = i.to_json(orient='records')
    with open(filename.replace('.json', '-clean.json'), 'w') as file:
        file.write(''.join(i))
