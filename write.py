#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import sys, random, re

SIZE_PATTERN = re.compile('(?P<size>\d+)(?P<unit>[GgMmKk])?B?')

REQ_SIZE_RANGE = (100, 50*1024*1024) #Bytes

#REQ_SIZE_RANGE = (100, 100*1024) #Bytes

C100 = 'C'*100

def human_bytes(b):
    UNIT = ('K', 'M', 'G', 'T')
    for i in xrange(len(UNIT), 0, -1):
        if b > 1024**i:
            return '%.2f%s' %(1.0*b/(1024**i), UNIT[i-1])
    return b

def parse_size_arg(arg_str):
    m = SIZE_PATTERN.match(arg_str)
    unit_n = 1
    if m:
        unit = m.group('unit')
        if unit:
            unit = unit.upper()
            if unit == 'K': unit_n = 1024
            elif unit == 'M': unit_n  = 1024*1024
            elif unit == 'G': unit_n = 1024*1024*1024
        size = int(m.group('size'))
        return size * unit_n
    raise ValueError('size format invalid: %s' %arg_str, 'in parse_size_arg()')
    return 0

def parse_req_size_range(range_str):
    if ',' in range_str:
        min_size, max_size = range_str.split(',')
        min_size, max_size = parse_size_arg(min_size), parse_size_arg(max_size)
    else:
        max_size = parse_size_arg(range_str)
        min_size = REQ_SIZE_RANGE[0]

    if min_size > max_size:
        raise ValueError('min_size > max_size!', 'in parse_req_size_range()')

    return (min_size, max_size)
        

def rand_req_size(filesize, req_size_range):
    maxsize = req_size_range[1]
    if req_size_range[1] > filesize: maxsize = filesize
    return random.randint(req_size_range[0], maxsize) 

def rand_req_offset(filesize, size):
    offset_range = (0, filesize - size)
    return random.randint(*offset_range)

if __name__ == '__main__':
    usage = 'python <filename> <filesize> <req_count> [[<req_min_size>,]<req_max_size>]'
    if len(sys.argv) not in (4, 5): 
        print usage
        exit()

    filesize = parse_size_arg(sys.argv[2])
    if not filesize:
        print usage
        exit()

    req_count = int(sys.argv[3])

    req_size_range = parse_req_size_range(sys.argv[4]) if len(sys.argv) == 5 else REQ_SIZE_RANGE

    print 'write %s, %s Bytes for %s times.' %(sys.argv[1], filesize, req_count)
    print 'req size between %s' %(req_size_range, )

    msg = raw_input('Continue?(Y/n) ')
    if msg not in ('Y', 'y'): exit()
    
    count = 0
    with open(sys.argv[1], 'wb') as f:
        f.truncate(filesize)
        while req_count > 0:
            count += 1
            size = rand_req_size(filesize, req_size_range)
            offset = rand_req_offset(filesize, size)
            print '%6s  offset:%12s bytes:%12s' %(count, offset, size)
            f.seek(offset, 0)
            for _ in xrange(size/len(C100)):
                f.write(C100)
            f.write('C'*(size%len(C100)))
            f.flush()
            req_count -= 1
    
    print 'Done.'
    
    	
