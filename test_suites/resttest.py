import requests
import json
from nose.tools import assert_equal


surl = 'https://my-json-server.typicode.com/jeevan449/pythonlearning'

class requestsexample:
    def __init__(self,url):
        self.surl = url   

    def getdata(self,path):
        self.path=path
        self.req=(self.surl+self.path)
        r = requests.get(self.req)
        data = r.json()
        code = r.status_code
        return data

    def postdata(self,path,params):
        self.params=params
        self.path=path
        self.url=self.surl+self.path
        r = requests.post(self.url,data = self.params)
        data1 = r.json()
        code = r.status_code
        return data1
    
obj = requestsexample(surl)
    
def test_postdata():
    path= '/posts'
    values = {'id':4, 'title':'jeevan'}
    res = obj.postdata(path,values)
    assert_equal(res['title'],'jeevan')
def test_getuserdata():
    path = '/posts/1'
    res = obj.getdata(path)
    assert_equal(res['title'],'Post 1')
def test_postdata_fail():
    path= '/posts'
    values = {'id':5, 'title':'chaitanya1'}
    res = obj.postdata(path,values)
    assert_equal(res['title'],'chaitanya')
def test_getuserdata_fail():
    path = '/posts/1'
    res = obj.getdata(path)
    assert_equal(res['title'],'Post 2')
