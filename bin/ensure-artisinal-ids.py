#!/usr/bin/env python

import sys
import os
import os.path
import json
import ArtisinalInts

import pprint

def crawl(options) :

    for root, dirs, files in os.walk(options.objects):

        for f in files:

            if not f.endswith(".json") :
                continue

            path = os.path.join(root, f)
            path = os.path.abspath(path)
            
            fh = open(path, 'r')
            data = json.load(fh)

            if data.get('artisinal:id', False):
                continue

            if not assign_int(data, options.provider):
                continue

            if data.get('brooklynintegers:id', False):
                del(data['brooklynintegers:id'])

            fh = open(path, 'w')
            json.dump(data, fh, indent=2)
            fh.close()

            print "update %s" % path

def assign_int(data, provider, max_tries=3):

    tries = 0

    while tries < max_tries:

        try:

            if provider == 'brooklyn':

                rsp = ArtisinalInts.get_brooklyn_integer()
                id = rsp[0]

                data[u'artisinal:id'] = id
                data[u'artisinal:provider'] = u'http://www.brooklynintegers.com/'
                return id

            elif provider == 'mission':

                rsp = ArtisinalInts.get_mission_integer()
                id = rsp[0]

                data[u'artisinal:id'] = id
                data[u'artisinal:provider'] = u'http://www.missionintegers.com/'
                return id

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
