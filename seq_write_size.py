#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import sys, os
from timeit import timeit

from write import parse_size_arg, human_bytes

def exec_req(f, size):
    C100 = 'C'*100
    for _ in xrange(size/len(C100)):
        f.write(C100)
    f.write('C'*(size%len(C100)))
    f.flush()
    os.fsync(f)

if __name__ == '__main__':
    usage = 'seq_write.py <filename> <filesize> <req_size> <req_count>'
    if len(sys.argv) != 5:
        print usage
        exit()

    filesize = parse_size_arg(sys.argv[2])
    req_size = parse_size_arg(sys.argv[3])
    req_count = int(sys.argv[4])

    print 'filename:%s filesize:%s req_size:%s req_count:%s' %(
                sys.argv[1], filesize, req_size, req_count)

    msg = raw_input('Continue?(Y/n) ')
    if msg not in ('Y', 'y'):  exit()

    time_cnt = 0
    bytes_cnt = 0
    with open(sys.argv[1], 'wb') as f:
        f.truncate(filesize)
        cnt = 0
        while cnt < req_count:
            cnt += 1

            if f.tell() + req_size > filesize:
                print 'Hit file end, seek to file start.'
                f.seek(0, 0)
                f.write('c')
                f.flush()
                os.fsync(f)

            t = timeit('exec_req(f, req_size)',
                           'from __main__ import f, req_size, exec_req, os',
                           number=1)                
            sys.stdout.write('\r%s/%s' %(cnt, req_count))
            sys.stdout.flush()
            bytes_cnt += req_size
            time_cnt += t

        print 'Done.'
        print 'Sum: %12s Bytes Time: %.4f seconds Bandwidth: %s Bps' %(
                    bytes_cnt, time_cnt, human_bytes(bytes_cnt/time_cnt))

        with open('sum', 'w') as  out:
            out.write('Sum: %12s Bytes Time: %.4f seconds Bandwidth: %s Bps' %(
                    bytes_cnt, time_cnt, human_bytes(bytes_cnt/time_cnt)))
            

        

