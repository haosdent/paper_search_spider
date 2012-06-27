#/usr/bin/env python
#coding:utf-8
'''
Created on 2012-6-22

@author: haosdent
'''
import sys
import contextlib, urllib2, urllib, chardet, cookielib, HTMLParser

def snatch(author, topic):
    cookies = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
    urllib2.install_opener(opener)
    req = urllib2.Request("http://www.webofknowledge.com/")
    resp = urllib2.urlopen(req)
    
    for cookie in cookies:
        if cookie.name == "SID":
            SID = cookie.value
            print SID
    
    postdata = {"fieldCount" : "3", "action" : "search",
                "product" : "UA",
                "search_mode" : "GeneralSearch",
                "SID" : SID,
                "max_field_count" : "25",
                "max_field_notice" : "Notice: You cannot add another field.",
                "input_invalid_notice" : "Search Error: Please enter a search term.",
                "input_invalid_notice_limits" : "<br/>Note: Fields displayed in scrolling boxes must be combined with at least one other search field.",
                "sa_params" : "UA|http://apps.webofknowledge.com/InboundService.do%3Fproduct%3DUA%26search_mode%3DGeneralSearch%26mode%3DGeneralSearch%26action%3Dtransfer%26viewType%3Dinput%26SID%3D4BjaEddMd3LHjgAb8LF%26inputbox%3Dinput???|4BjaEddMd3LHjgAb8LF||[name=AU;value=initAuthor;keyName=;type=termList;priority=10, name=GP;value=initGroupAuthor;keyName=;type=termList;priority=10, name=SO;value=initSource;keyName=;type=termList;priority=10]'",
                "sa_img_alt" : "Select terms from the index",
                "value(input1)" : topic,
                "value(select1)" : "TS",
                "value(hidInput1)" : "initVoid",
                "value(hidShowIcon1)" : "0",
                "value(bool_1_2)" : "AND",
                "value(input2)" : author,
                "value(select2)" : "AU",
                "value(hidInput2)" : "initAuthor",
                "value(hidShowIcon2)" : "1",
                "value(bool_2_3)" : "AND",
                "value(input3)" : "",
                "value(select3)" : "",
                "value(hidInput3)" : "initSource",
                "value(hidShowIcon3)" : "1",
                "x" : "22",
                "y" : "18",
                "limitStatus" : "collapsed",
                "expand_alt" : "Expand these settings",
                "expand_title" : "Expand these settings",
                "collapse_alt" : "Collapse these settings",
                "collapse_title" : "Collapse these settings",
                "SinceLastVisit_UTC" : "",
                "SinceLastVisit_DATE" : "",
                "timespanStatus:display" : "block",
                "timeSpanCollapsedListStatus" : "display: none",
                "period" : "Range Selection",
                "range" : "ALL",
                "startYear" : "1950",
                "endYear" : "2012",
                "ssStatus" : "display:none",
                "ss_lemmatization" : "On",
                "ss_query_language" : "",
                "rsStatus" : "display:none",
                "rs_rec_per_page" : "10",
                "rs_sort_by" : "PY.D;LD.D;SO.A;VL.D;PG.A;AU.A",
                "rs_refinePanel" : "visibility:show"}
    
    postdata = urllib.urlencode(postdata)
    req = urllib2.Request("http://apps.webofknowledge.com/UA_GeneralSearch.do", postdata)
    resp = urllib2.urlopen(req)
        
    resp_body = resp.read()
    start_index = resp_body.find('/full_record.do?')
    end_index = resp_body.find('">\n<value lang_id="">')
    html_parser = HTMLParser.HTMLParser()
    result_url = "http://apps.webofknowledge.com" + resp_body[start_index : end_index]
    result_url = html_parser.unescape(result_url)
    print result_url
    
    req = urllib2.Request(result_url)
    resp = urllib2.urlopen(req)
    
    resp_body = resp.read()
    encoding = chardet.detect(resp_body)["encoding"]
    if encoding == "GB2312":
        resp_body = resp_body.decode('gbk').encode('utf-8')
    elif encoding == "UTF8":
        resp_body = resp_body.decode('utf-8')
    
    return resp_body
    
if __name__ == '__main__':
    snatch("Wu H", "Complete chloroplast genome sequence of Magnolia kwangsiensis")