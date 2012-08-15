''' Interface to hand-crafted integers from Brooklyn and San Francisco.

ArtisinalInts includes functions for retrieving numbers from online integers
sources Mission Integers and Brooklyn Integers. Each service's API is used to
generate unique new numbers:

    http://missionintegers.com/api.html
    http://brooklynintegers.com/api/

The get_* functions return values, while the iter_* functions return iterators
that can be used in loops to get a stream of new numbers.
'''
from httplib import HTTPConnection
from urllib import urlencode
from urlparse import urljoin
from json import loads

__version__ = '1.0.0'

def _request_mission_next_int(body):
    '''
    '''
    head = {'Content-Type': 'application/x-www-form-urlencoded'}
    conn = HTTPConnection('missionintegers.com', 80)
    conn.request('POST', '/next-int', body, head)
    
    return conn.getresponse()

def get_mission_integers(count):
    ''' Ask Mission Integers for a list of integers.
    
        Returns a list of integers; count is limited to 10 by the server.
    '''
    body = 'format=json&count=%d' % count
    resp = _request_mission_next_int(body)
    
    if resp.status not in range(200, 299):
        raise Exception()
    
    return loads(resp.read())

def get_mission_integer():
    ''' Ask Mission Integers for a single integer.
    
        Returns a tuple with number and integer permalink.
    '''
    body = 'format=json'
    resp = _request_mission_next_int(body)
    
    if resp.status not in range(200, 299):
        raise Exception('Non-2XX response code from the Mission: %d' % resp.status)
    
    value = loads(resp.read())[0]
    href = urljoin('http://missionintegers.com', resp.getheader('Location'))
    
    return value, href

def iter_mission_integers():
    ''' Generate a stream of Mission Integers, forever.
    
        Returns an iterator:
        http://docs.python.org/library/stdtypes.html#typeiter.
    '''
    # start with a small number
    count = 1
    
    while True:
        for integer in get_mission_integers(count):
            yield integer
        
        # get more next time
        count = min(5, count + 1)

def get_brooklyn_integer():
    ''' Ask Brooklyn Integers for a single integer.
    
        Returns a tuple with number and integer permalink.
    '''
    body = 'method=brooklyn.integers.create'
    head = {'Content-Type': 'application/x-www-form-urlencoded'}
    conn = HTTPConnection('api.brooklynintegers.com', 80)
    conn.request('POST', '/rest/', body, head)
    resp = conn.getresponse()
    
    if resp.status not in range(200, 299):
        raise Exception('Non-2XX response code from Brooklyn: %d' % resp.status)
    
    data = loads(resp.read())
    value = data['integer']
    href = data['shorturl']
    
    return value, href

def iter_brooklyn_integers():
    ''' Generate a stream of Brooklyn Integers, forever.
    
        Returns an iterator:
        http://docs.python.org/library/stdtypes.html#typeiter.
    '''
    while True:
        integer, href = get_brooklyn_integer()
        yield integer
