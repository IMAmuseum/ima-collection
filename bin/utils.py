import pprint
import os.path
import string
import unicodedata

import logging
import json
import csv
import types

def dumper(data):
    print pprint.pformat(data)

def id2path(id):

    tmp = str(id)
    parts = []

    while len(tmp) > 3:
        parts.append(tmp[0:3])
        tmp = tmp[3:]

    if len(tmp):
        parts.append(tmp)

    return os.path.join(*parts)

def clean_meta_name(name, allow_punctuation=[]):

    name = name.strip()
    name = name.lower()
    
    name = remove_accents(name)

    for c in string.punctuation:

        if c in allow_punctuation:
            continue

        name = name.replace(c, "")

    name = name.replace(" ", "-")
    name = name.replace("--", "-")
        
    return name

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii

# This does what it sounds like - it flattens directory of
# key/value JSON files in to a CSV file. If your data is more
# complicated than that you shouldn't be using this...

def jsondir2csv(datadir, outfile):

    fh = open(outfile, 'w')
    writer = None

    for root, dirs, files in os.walk(datadir):

        for f in files:

            path = os.path.join(root, f)
            logging.info("processing %s" % path)
    
            data = json.load(open(path, 'r'))

            if not writer:
                keys = data.keys()
                keys.sort()
                writer = csv.DictWriter(fh, fieldnames=keys)
                writer.writeheader()

            try:
                writer.writerow(data)
            except Exception, e:
                logging.error(e)

    logging.info("done");

def utf8ify_dict(stuff):
    
    for k, v in stuff.items():

        if v and type(v) == types.UnicodeType:
            try:
                v = v.encode('utf8')
            except Exception, e:
                logging.error(e)
                v = ''

        stuff[k] = v

    return stuff
