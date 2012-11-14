#!/usr/bin/env python

import sys
import json
import csv
import os
import os.path
import types

import utils

import logging
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':

    whoami = os.path.abspath(sys.argv[0])

    bindir = os.path.dirname(whoami)
    rootdir = os.path.dirname(bindir)

    datadir = os.path.join(rootdir, 'json/actors')
    metadir = os.path.join(rootdir, 'meta')

    outfile_actors = os.path.join(metadir, 'actors.csv')

    fh_actors = open(outfile_actors, 'w')

    writer_actors = None

    for root, dirs, files in os.walk(datadir):

        for f in files:

            path = os.path.join(root, f)
            logging.info("processing %s" % path)
    
            data = json.load(open(path, 'r'))

            data['ulan:id'] = data['ULAN']['UlanIdNo']
            data['ulan:name'] = data['ULAN']['Name']
            del(data['ULAN'])

            if not writer_actors:

                keys = data.keys()
                keys.sort()

                writer_actors = csv.DictWriter(fh_actors, fieldnames=keys)
                writer_actors.writeheader()

            data = utils.utf8ify_dict(data)
            writer_actors.writerow(data)

    logging.info("done");
            
