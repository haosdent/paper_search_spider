#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-6-22

@author: haosdent
'''
import pymongo

conn = pymongo.Connection()
queue = conn.paper_search_spider.queue

def count():
    return queue.count()

def find_one(status = "uncompleted"):
    
    order = None
    
    if status == "uncompleted":
        order = queue.find_one({"$or" : [{"status" : status}, {"status" : "never"}]})
    elif status == "completed" or status == "using":
        order = queue.find_one({"status" : status})
    else:
        order = queue.find_one()
    
    return order

def find(skip = 0, limit = 0, status = "uncompleted"):
    orders = None
    
    if status == "uncompleted":
        orders = queue.find({"$or" : [{"status" : status}, {"status" : "never"}]}, skip = skip, limit = limit)
    elif status == "completed" or status == "using":
        orders = queue.find({"status" : status}, skip = skip, limit = limit)
    else:
        orders = queue.find(skip = skip, limit = limit)
        
    return orders

def change_status(order):
    queue.update({"_id" : order["_id"]}, {"$set" : {"status" : order["status"]}})

def update_response(order):
    queue.update({"_id" : order["_id"]}, {"$set" : {"response" : order["response"], "status" : "completed"}})

def insert_one(order):
    
    """
    TODO add check.
    
    Check if the format of order is normal.
    """
    if order != None:
        queue.insert(order)
        
def init_db():
    if count() == 0:
        order = {"type" : "EI", "author" : "Hongzhi", "topic" : "Rectangular Tree Browser", "status" : "never"}
        print "Start initialize database."
        for i in xrange(0, 100):
            queue.insert(order, manipulate = False)
        print "Finished initialize data to database."