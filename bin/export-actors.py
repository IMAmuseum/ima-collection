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

            if not data.get('actors', False):
                continue

            for a in data['actors']:

                id = a.get('irn', None)

                if not id:
                    continue

                role = a.get('role', 'unknown')

                if not role:
                    role = 'unknown'

                role = utils.clean_meta_name(role)

                dirname = os.path.join(actors, role)

                if not os.path.exists(dirname):
                    os.makedirs(dirname)

                fname = "%s.json" % id

                apath = os.path.join(dirname, fname)

                if os.path.exists(apath):
                    continue

                fh = open(apath, 'w')
                json.dump(a, fh, indent=2)
                fh.close()

            for p in data['publishers']:

                id = p.get('irn', None)

                if not id:
                    continue

                role = a.get('role', 'unknown')

                if not role:
                    role = 'unknown'

                role = 'publisher'

                dirname = os.path.join(actors, role)

                if not os.path.exists(dirname):
                    os.makedirs(dirname)

                fname = "%s.json" % id

                ppath = os.path.join(dirname, fname)

                if os.path.exists(ppath):
                    continue

                fh = open(ppath, 'w')
                json.dump(p, fh, indent=2)
                fh.close()

            for p in data['printers']:

                id = p.get('irn', None)

                if not id:
                    continue

                role = a.get('role', 'unknown')

                if not role:
                    role = 'unknown'

                role = 'printer'

                dirname = os.path.join(actors, role)

                if not os.path.exists(dirname):
                    os.makedirs(dirname)

                fname = "%s.json" % id

                ppath = os.path.join(dirname, fname)

                if os.path.exists(ppath):
                    continue

                fh = open(ppath, 'w')
                json.dump(p, fh, indent=2)
                fh.close()

if __name__ == '__main__':

    whoami = os.path.abspath(sys.argv[0])

    bindir = os.path.dirname(whoami)
    rootdir = os.path.dirname(bindir)

    objects_dir = os.path.join(rootdir, 'json/objects')
    actors_dir = os.path.join(rootdir, 'json/actors')

    crawl(objects_dir, actors_dir)
