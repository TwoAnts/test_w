#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import sys, re, os
from timeit import timeit

from write import human_bytes
from plot import plot_req_time, plot_line_chart

STAT_PATTERN = re.compile(
            '\s*filesize:\s*(?P<filesize>\d+)\s*req_count:\s*(?P<req_count>\d+).*')

REQ_PATTERN = re.compile(
            '\s*(?P<count>\d+)\s*offset:\s*(?P<offset>\d+)\s*bytes:\s*(?P<size>\d+).*')


def exec_req(f, offset, size):
    C100 = 'C'*100
    f.seek(offset, 0)
    for _ in xrange(size/len(C100)):
        f.write(C100)
    f.write('C'*(size%len(C100)))
    f.flush()
    os.fsync(f)

if __name__ == '__main__':
    usage = 'run_write.py <seq_file> <test_file>'
    if len(sys.argv) != 3:
        print usage
        exit()


    filesize = 0
    req_count = 0
    with open(sys.argv[1], 'r') as f:
        nr_content = 0
        for line in f:
            line = line.strip()
            if line[0] == '#': continue 

            m = STAT_PATTERN.match(line)
            if m:
                filesize = int(m.group('filesize'))
                req_count = int(m.group('req_count'))
                break


        print 'test_file:%s filesize:%s req_count:%s' %(
                                sys.argv[2], filesize, req_count)
        msg = raw_input('Continue?(Y/n) ')
        if msg not in ('Y', 'y'): exit()

        bytes_sum = 0
        time_sum = 0
        history = []
        last_bs = 0
        last_time = 0
        avg_rate = 0
        rates = []
        times = []
        avg_flag = False
        with open(sys.argv[2], 'wb') as target:
            target.truncate(filesize)
            for line in f:
                m = REQ_PATTERN.match(line)
                if not m: continue
                cnt = int(m.group('count'))
                offset = int(m.group('offset'))
                size = int(m.group('size'))

                t = timeit('exec_req(target, offset, size)',
                           'from __main__ import target, offset, size, exec_req, os',
                           number=1)                
                times.append(t)

                while last_time >= 1: 
                    bs, time = history.pop(0)
                    last_bs -= bs
                    last_time -= time
                    
                history.append((size, t))
                last_bs += size
                last_time += t
                if not avg_flag and last_time >= 1: avg_flag = True
                if last_time >= 1 or not avg_flag:
                    avg_rate = last_bs/last_time
                rates.append(avg_rate)
                
                
                sys.stdout.write('\r%s/%s, %sBps' %(cnt, req_count, human_bytes(avg_rate)))
                sys.stdout.flush()

                #print '%-6s offset:%-12s bytes:%-12s time: %s seconds' %(cnt, offset, size, t)
                bytes_sum += size
                time_sum += t
        
        print '\nDone. Sum: %12s Bytes Time: %.4f seconds Bandwidth: %s Bps' %(
                    bytes_sum, time_sum, human_bytes(bytes_sum/time_sum))

        #fname = plot_req_time(times, title='req_times', ymax=time_sum/req_count*2.5,
        #                                                                 draw_avg=True)
        #print 'Save req_times pictrue to %s.' %fname 

        fname = plot_line_chart(rates, 'Bps', 'Count', 'rates', ymax=bytes_sum/time_sum*2.5,
                                                                         draw_avg=True)
        print 'Save rates picture to %s.' %fname
        


        with open('sum', 'w') as out:
            out.write('Sum: %12s Bytes Time: %.4f seconds Bandwidth: %s Bps' %(
                    bytes_sum, time_sum, human_bytes(bytes_sum/time_sum)))
            
                
            
                
            
