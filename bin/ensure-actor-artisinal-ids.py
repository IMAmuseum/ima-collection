#!/usr/bin/env python

import sys
import os
import os.path
import json
import ArtisinalInts

artists = {}

def crawl(options) :

    for root, dirs, files in os.walk(options.objects):

        for f in files:

            if not f.endswith(".json") :
                continue

            path = os.path.join(root, f)
            path = os.path.abspath(path)
            
            fh = open(path, 'r')
            data = json.load(fh)

            if not data.get('actors', False):
                continue

            has_updates = False

            for a in data['actors']:

                name = a['name']
                id = None

                if artists.get(name, False):
                    id = artists[name]
                else:
                    id = get_int(options.provider)

                if not id:
                    continue

                artists[name] = id

                a['artisinal:id'] = id
                a['artisinal:provider'] = 'http://www.brooklynintegers.com/'

                has_updates = True

            if not has_updates:
                continue

            fh = open(path, 'w')
            json.dump(data, fh, indent=2)
            fh.close()

            print "update %s" % path

def get_int(provider, max_tries=3):

    tries = 0

    while tries < max_tries:

        try:

            if provider == 'brooklyn':

                rsp = ArtisinalInts.get_brooklyn_integer()
                return rsp[0]
            
            elif provider == 'mission':

                rsp = ArtisinalInts.get_mission_integer()
                return rsp[0]

            else:

                return None

        except Exception, e:
            pass
            
        tries += 1

    return None



if __name__ == '__main__':

    import optparse

    parser = optparse.OptionParser(usage="...")

    parser.add_option('--objects', dest='objects',
                        help='The path to your collection objects',
                        action='store')

    parser.add_option('--provider', dest='provider',
                        help="The name of your artisinal ID provider. Valid options are 'mission' and 'brooklyn'",
                        action='store')

    options, args = parser.parse_args()

    crawl(options)
