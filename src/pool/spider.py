#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-6-18

@author: haosdent
'''
import gevent
from gevent import monkey
from gevent.pool import Pool
from db import queue
from pool import httpclient
from pool.httpclient import HttpClientPool

monkey.patch_all()

""" Counter variable """
count = 0

""" Create the thead pool which size is 1000 """
thead_pool = Pool(10)

"""
In spider cluster, 
spider_serial_number is the serial number of this spider node while
spider_total_number is the size of spider cluster. 
"""
spider_serial_number = 0
spider_total_number = 1

def spider():
    """ Create the httpclient pool which default size is 1200 """
    httpclient_pool = HttpClientPool()
    
    """
    Allocate a task to this spider node,
    skip is the task's start point in queue,
    and limit is the number of data which will be snatched in this spider node.
    """
    queue_size = queue.count()
    limit = queue_size / spider_total_number 
    skip = limit * spider_serial_number
    if spider_total_number - 1 == spider_serial_number:
        limit += queue_size % spider_total_number
        
    print "skip = ", skip, ", limit = ", limit
    
    with gevent.Timeout(None, False):        
        print "This spider is start."
        
        orders = queue.find(skip, limit)
        while orders.count() > 0:
            for order in orders:
                thead_pool.spawn(httpclient_pool.request, order)
            thead_pool.join()
            
            print "Start =", httpclient.start,", End =", httpclient.end,", Error =", httpclient.error
            httpclient.start = 0
            httpclient.end = 0
            httpclient.error = 0
            
            orders = queue.find(skip, limit)
            
        print "This spider is finished."

if __name__ == '__main__':
    queue.init_db()
    spider()




