#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-6-22

@author: haosdent
'''
import re, sys, contextlib, urllib2, urllib, chardet, cookielib, HTMLParser
from geventhttpclient import HTTPClient
from geventhttpclient.url import URL

def snatch(httpclient, order):
    author = order["author"]
    topic = order["topic"]
    
    """ Firstly, register a EISESSION in www.engineeringvillage2.org """
    resp = httpclient.get("http://www.engineeringvillage2.org/controller/servlet/Controller")
    location = resp.headers[4][1]
    location = re.sub(r'quickSearch\S+', r'expertSearchCitationFormat', location)
    
    """ Secondly, post the query condition to location which get from first step
        and then get the url on first position in the search result. """
    headers = {"Content-Length" : "298",
               "Content-Type" : "application/x-www-form-urlencoded"}
    postdata = [("database", "1"),
                ("database", "32768"),
                ("database", "16384"),
                ("searchWord1", "{" + topic + "} WN TI AND {" + author + "} WN AU"),
                ("yearselect", "yearrange"),
                ("startYear", "1790"),
                ("endYear", "2012"),
                ("stringYear", "CSY1969CST1969USY1790UST1790ESY1978EST1978"),
                ("updatesNo", "1"),
                ("sort", "relevance"),
                ("autostem", "on"),
                ("search", "Search")]
    postdata = urllib.urlencode(postdata)
    resp = httpclient.post(location, postdata, headers)
    
    """ Parser the result url from HTML format to normal format. """
    resp_body = resp.read()
    result_url = re.search(r'<a class="LgBlueLink" TITLE="Detailed"[ \S]+HREF="([\S]+)"', resp_body)
    if result_url == None:
        result = {"status_code" : resp.status_code,"body" : None}
    else:
        html_parser = HTMLParser.HTMLParser()
        result_url = html_parser.unescape("http://www.engineeringvillage2.org/" + result_url.group(1))
    
        """ Thirdly, get the page of result_url. """
        resp = httpclient.get(result_url)
        resp_body = resp.read()
        result = {"status_code" : resp.status_code,"body" : resp_body}
        
    """ Finally, return the order with result. """
    order["response"] = result
    return order