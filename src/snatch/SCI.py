#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-6-22

@author: haosdent
'''
import re, sys, contextlib, urllib2, urllib, chardet, cookielib, HTMLParser, geventhttpclient.httplib
from geventhttpclient import HTTPClient
from geventhttpclient.url import URL
geventhttpclient.httplib.patch()
import httplib2

def snatch(httpclient, order):
    author = "Wu H"
    topic = "Complete chloroplast genome sequence of Magnolia kwangsiensis"

    error_count = -1
    
    while error_count != 0:
        error_count = -1
        """ Firstly, register a SID in www.webofknowledge.com and get it. """
        headers = {"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Charset" : "UTF-8,*;q=0.5",
                   "Accept-Encoding" : "gzip,deflate,sdch",
                   "Accept-Language" : "en-US,en;q=0.8",
                   "Connection" : "keep-alive",
                   "Cookie" : 'CUSTOMER="South China Agricultural University"; E_GROUP_NAME="South China Agricultural University"',
                   "Host" : "www.webofknowledge.com",
                   "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.42 Safari/536.11"}    
        httpclient = HTTPClient("www.webofknowledge.com", concurrency=10)
        resp = httpclient.get("http://www.webofknowledge.com/", headers = headers)
        while re.search(r'SID=([%\w]+)', resp.headers[4][1]) == None and re.search(r'SID=([%\w]+)', resp.headers[3][1]) == None and error_count <= 5:
            error_count +=1
            resp = httpclient.get("http://www.webofknowledge.com/", headers = headers)
        if error_count > 5:
            continue
        else:
            error_count = 0
        if re.search(r'SID=([%\w]+)', resp.headers[4][1]) != None:
            SID = re.search(r'SID=([%\w]+)', resp.headers[4][1]).group(1)
        elif re.search(r'SID=([%\w]+)', resp.headers[3][1]) != None:
            SID = re.search(r'SID=([%\w]+)', resp.headers[3][1]).group(1)
        print SID
        
        """ Secondly, post the query condition to www.webofknowledge.com
            and then get the url on first position in the search result. """
        headers = {"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Charset" : "UTF-8,*;q=0.5",
                   "Accept-Encoding" : "gzip,deflate,sdch",
                   "Accept-Language" : "en-US,en;q=0.8",
                   "Cache-Control" : "max-age=0",
                   "Connection" : "keep-alive",
                   "Content-Length" : "1908",
                   "Content-Type" : "application/x-www-form-urlencoded",
                   "Cookie" : 'SID="' + SID + '"; CUSTOMER="South China Agricultural University"; E_GROUP_NAME="South China Agricultural University"',
                   "Host" : "apps.webofknowledge.com",
                   "Origin" : "http://apps.webofknowledge.com",
                   "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.42 Safari/536.11"}
        postdata = [("fieldCount", "3"),
                    ("action", "search"),
                    ("product", "UA"),
                    ("search_mode", "GeneralSearch"),
                    ("SID", SID),
                    ("max_field_count", "25"),
                    ("max_field_notice", "Notice: You cannot add another field."),
                    ("input_invalid_notice", "Search Error: Please enter a search term."),
                    ("input_invalid_notice_limits", "<br/>Note: Fields displayed in scrolling boxes must be combined with at least one other search field."),
                    ("sa_params", "UA|http://apps.webofknowledge.com/InboundService.do%3Fproduct%3DUA%26search_mode%3DGeneralSearch%26mode%3DGeneralSearch%26action%3Dtransfer%26viewType%3Dinput%26SID%3D" + SID + "%26inputbox%3Dinput???|" + SID + "||[name=AU;value=initAuthor;keyName=;type=termList;priority=10, name=GP;value=initGroupAuthor;keyName=;type=termList;priority=10, name=SO;value=initSource;keyName=;type=termList;priority=10]'"),
                    ("sa_img_alt", "Select terms from the index"),
                    ("value(input1)", topic),
                    ("value(select1)", "TS"),
                    ("value(hidInput1)", "initVoid"),
                    ("value(hidShowIcon1)", "0"),
                    ("value(bool_1_2)", "AND"),
                    ("value(input2)", author),
                    ("value(select2)", "AU"),
                    ("value(hidInput2)", "initAuthor"),
                    ("value(hidShowIcon2)", "1"),
                    ("value(bool_2_3)", "AND"),
                    ("value(input3)", ""),
                    ("value(select3)", "SO"),
                    ("value(hidInput3)", "initSource"),
                    ("value(hidShowIcon3)", "1"),
                    ("x", "71"),
                    ("y", "15"),
                    ("limitStatus", "collapsed"),
                    ("expand_alt", "Expand these settings"),
                    ("expand_title", "Expand these settings"),
                    ("collapse_alt", "Collapse these settings"),
                    ("collapse_title", "Collapse these settings"),
                    ("SinceLastVisit_UTC", ""),
                    ("SinceLastVisit_DATE", ""),
                    ("timespanStatus", "display: block"),
                    ("timeSpanCollapsedListStatus", "display: none"),
                    ("period", "Range Selection"),
                    ("range", "ALL"),
                    ("startYear", "1950"),
                    ("endYear", "2012"),
                    ("ssStatus", "display:none"),
                    ("ss_lemmatization", "On"),
                    ("ss_query_language", ""),
                    ("rsStatus", "display:none"),
                    ("rs_rec_per_page", "10"),
                    ("rs_sort_by", "PY.D;LD.D;SO.A;VL.D;PG.A;AU.A"),
                    ("rs_refinePanel", "visibility:show")]
        postdata = urllib.urlencode(postdata)
        resp = httpclient.post("http://apps.webofknowledge.com/UA_GeneralSearch.do", postdata, headers)
        while re.search(r'JSESSIONID=([\w]+)', resp.headers[1][1]) == None and error_count <= 5:
            print "POST"
            print resp.headers
            error_count += 1
            resp = httpclient.post("http://apps.webofknowledge.com/UA_GeneralSearch.do", postdata, headers)
        if error_count > 5:
            continue
        else:
            error_count = 0
        headers = {"Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                   "Accept-Charset" : "UTF-8,*;q=0.5",
                   "Accept-Encoding" : "gzip,deflate,sdch",
                   "Accept-Language" : "en-US,en;q=0.8",
                   "Cache-Control" : "max-age=0",
                   "Connection" : "keep-alive",
                   "Cookie" : 'SID="' + SID + '"; CUSTOMER="South China Agricultural University"; E_GROUP_NAME="South China Agricultural University"',
                   "Host" : "apps.webofknowledge.com",
                   "User-Agent" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.42 Safari/536.11"}
        result_url = "http://apps.webofknowledge.com/summary.do?SID=" + SID +"&product=UA&qid=1&search_mode=GeneralSearch"
        while re.search(r'JSESSIONID=([\w]+)', resp.headers[1][1]) != None and error_count <= 5:
            print "GET"
            error_count += 1
            JSESSIONID = re.search(r'JSESSIONID=([\w]+)', resp.headers[1][1]).group(1)
            headers["Cookie"] = 'SID="' + SID + '"; CUSTOMER="South China Agricultural University"; E_GROUP_NAME="South China Agricultural University"; JSESSIONID=' + JSESSIONID
            resp = httpclient.get(result_url, headers = headers)
            print resp.headers
            print headers["Cookie"]
        if error_count > 5 or re.search(r'location', resp.headers[2][0]) != None or re.search(r'location', resp.headers[3][0]) != None:
            continue
        else:
            error_count = 0
        print resp.read()
    
    """ Parser the result url from HTML format to normal format. """
#    resp_body = resp.read()
#    print resp_body
#    result_url = re.search(r'<a class="LgBlueLink" TITLE="Detailed"[ \S]+HREF="([\S]+)"', resp_body)
#    if result_url == None:
#        result = {"status_code" : resp.status_code,"body" : None}
#    else:
#        html_parser = HTMLParser.HTMLParser()
#        result_url = html_parser.unescape("http://www.engineeringvillage2.org/" + result_url.group(1))
#    
#        """ Thirdly, get the page of result_url. """
#        resp = httpclient.get(result_url)
#        resp_body = resp.read()
#        result = {"status_code" : resp.status_code,"body" : resp_body}
#        
#    """ Finally, return the order with result. """
#    order["response"] = result
#    return order

if __name__ == '__main__':
    snatch(None, None)