#!/usr/bin/env python

import sys
import os
import os.path
import json
import utils

def crawl(options) :

    objects = os.path.abspath(options.objects)
    actors = os.path.abspath(options.actors)

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

                # see also: ensure-artisinal-ids.py

                id = a.get('artisinal:id', None)

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

if __name__ == '__main__':

    import optparse

    parser = optparse.OptionParser(usage="...")

    parser.add_option('--objects', dest='objects',
                        help='The path to your collection objects',
                        action='store')

    parser.add_option('--actors', dest='actors',
                        help="The path to your collection actors",
                        action='store')

    options, args = parser.parse_args()

    crawl(options)
