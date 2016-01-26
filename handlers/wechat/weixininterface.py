#coding:UTF-8
import hashlib
import web
import lxml
import os
import time
import urllib2
import json
from lxml import etree

def youdao(word):
    qword = urllib2.quote(word)
    baseurl =r'http://fanyi.youdao.com/openapi.do?keyfrom=pyworm&key=973100900&type=data&doctype=json&version=1.1&q='
    url = baseurl+qword
    resp = urllib2.urlopen(url)
    fanyi = json.loads(resp.read())
    if fanyi['errorCode'] == 0:
        if 'basic' in fanyi.keys():
            array1 = []
            array2 = []
            for item1 in fanyi['basic']['explains']:
                array1.append(item1+'\n')
            for item2 in fanyi['web'][0]['value']:
                array2.append(item2+'\n')
            if 'phonetic' in fanyi['basic']:
                #trans = u'%s:\n%s\n%s\n网络释义：\n%s'%(fanyi['query'],''.join(fanyi['translation']),' '.join(fanyi['basic']['explains']),''.join(fanyi['web'][0]['value']))
                trans = u'%s:\n%s\n%s\n%s\n%s\n%s%s\n%s'%(fanyi['query'],''.join('-' * 3 + u'翻译' + '-' * 3),''.join(fanyi['translation']),''.join('-' * 3 + u'词典' + '-' * 3),''.join(fanyi['basic']['phonetic']),''.join(array1),''.join('-' * 3 + u'网络释义' + '-' * 3),''.join(array2))
            else:
                trans = u'%s:\n%s\n%s\n%s\n%s%s\n%s'%(fanyi['query'],''.join('-' * 3 + u'翻译' + '-' * 3),''.join(fanyi['translation']),''.join('-' * 3 + u'词典' + '-' * 3),''.join(array1),''.join('-' * 3 + u'网络释义' + '-' * 3),''.join(array2))


            return trans
        else:
            trans =u'%s:\n基本翻译:%s\n'%(fanyi['query'],''.join(fanyi['translation']))
            return trans
    elif fanyi['errorCode'] == 20:
        return u'对不起，要翻译的文本过长'
    elif fanyi['errorCode'] == 30:
        return u'对不起，无法进行有效的翻译'
    elif fanyi['errorCode'] == 40:
        return u'对不起，不支持的语言类型'
    else:
        return u'对不起，您输入的单词%s无法翻译,请检查拼写'% word

class WeixinInterface:
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root,'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        data = web.input()
        signature=data.signature
        timestamp=data.timestamp
        nonce=data.nonce
        echostr=data.echostr
        token="pychat"
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
        if hashcode == signature:
            return echostr

    def POST(self):
        str_xml=web.data()
        xml=etree.fromstring(str_xml)
        content=xml.find("Content").text
        msgType=xml.find("MsgType").text
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        if type(content).__name__ == "unicode":
            content = content.encode('UTF-8')
        Nword = youdao(content)
        return self.render.reply_text(fromUser,toUser,int(time.time()),Nword)



