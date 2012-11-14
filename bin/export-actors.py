#!/usr/bin/env python

import sys
import os
import os.path
import json
import utils

def crawl(objects, actors) :

    for root, dirs, files in os.walk(objects):

        for f in files:

            if not f.endswith(".json") :
                continue

            path = os.path.join(root, f)
            path = os.path.abspath(path)
            
            fh = open(path, 'r')
            data = json.load(fh)

            for role in ('actors', 'printers', 'publishers') :

                if not data.get(role, False):
                    continue

                for a in data[ role ]:

                    id = a.get('irn', None)

                    if not id:
                        continue

                    parent = utils.id2path(id)
                    dirname = os.path.join(actors, parent)

                    if not os.path.exists(dirname):
                        os.makedirs(dirname)

                    fname = "%s.json" % id

                    path = os.path.join(dirname, fname)

                    if os.path.exists(path):
                        continue

                    fh = open(path, 'w')
                    json.dump(a, fh, indent=2)
                    fh.close()

if __name__ == '__main__':

    whoami = os.path.abspath(sys.argv[0])

    bindir = os.path.dirname(whoami)
    rootdir = os.path.dirname(bindir)

    objects_dir = os.path.join(rootdir, 'json/objects')
    actors_dir = os.path.join(rootdir, 'json/actors')

    crawl(objects_dir, actors_dir)
