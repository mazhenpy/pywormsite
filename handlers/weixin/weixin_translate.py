import hashlib
import logging
from urllib.parse import quote
import time
import json
import xml.etree.ElementTree as ET

import requests
import tornado.httpserver
import tornado.options
import tornado.web
import tornado.gen
import tornado.httpclient
from tornado.httpclient import HTTPClient

from pywormsite import config

request_log = logging.getLogger('request')

def youdao(word):
    qword = quote(word)
    baseurl = r'http://fanyi.youdao.com/openapi.do?keyfrom=pyworm&key=973100900&type=data&doctype=json&version=1.1&q='
    url = baseurl + qword
    http_client = HTTPClient()
    response = http_client.fetch(url, method='GET', request_timeout=120)
    fanyi = json.loads(response.body.decode())
    if fanyi['errorCode'] == 0:
        if 'basic' in fanyi.keys():
            array1 = []
            array2 = []
            for item1 in fanyi['basic']['explains']:
                array1.append(item1 + '\n')
            for item2 in fanyi['web'][0]['value']:
                array2.append(item2 + '\n')
            if 'phonetic' in fanyi['basic']:
                # trans = u'%s:\n%s\n%s\n网络释义：\n%s'%(fanyi['query'],''.join(fanyi['translation']),' '.join(fanyi['basic']['explains']),''.join(fanyi['web'][0]['value']))
                trans = u'%s:\n%s\n%s\n%s\n%s\n%s%s\n%s' % (
                    fanyi['query'], ''.join('-' * 3 + u'翻译' + '-' * 3),
                    ''.join(fanyi['translation']),
                    ''.join('-' * 3 + u'词典' + '-' * 3), ''.join(fanyi['basic']['phonetic']),
                    ''.join(array1),
                    ''.join('-' * 3 + u'网络释义' + '-' * 3), ''.join(array2))
            else:
                trans = u'%s:\n%s\n%s\n%s\n%s%s\n%s' % (
                    fanyi['query'], ''.join('-' * 3 + u'翻译' + '-' * 3),
                    ''.join(fanyi['translation']),
                    ''.join('-' * 3 + u'词典' + '-' * 3), ''.join(array1),
                    ''.join('-' * 3 + u'网络释义' + '-' * 3),
                    ''.join(array2))

            return trans
        else:
            trans = u'%s:\n基本翻译:%s\n' % (fanyi['query'], ''.join(fanyi['translation']))
            return trans
    elif fanyi['errorCode'] == 20:
        return u'对不起，要翻译的文本过长'
    elif fanyi['errorCode'] == 30:
        return u'对不起，无法进行有效的翻译'
    elif fanyi['errorCode'] == 40:
        return u'对不起，不支持的语言类型'
    else:
        return u'对不起，您输入的单词%s无法翻译,请检查拼写' % word


class Daiwan(object):
    """docstring for Daiwan."""

    BASE_URL = 'http://lolapi.games-cube.com'
    USER_API_URL = '/UserArea'
    USER_HOT_INFO_URL = '/UserHotInfo'
    BATTLT_SUMMARY_INFO = '/BattleSummaryInfo'
    CHAMPION = '/champion'

    def __init__(self):
        self.config = config()

        self.token = self.config["LOL"]["token"]
        self.headers = {'DAIWAN-API-TOKEN': self.token}

    def get_user_info(self, username):
        return requests.get(self.BASE_URL + self.USER_API_URL + '?keyword=' + username,
                            headers=self.headers).json()

    def get_user_hot_info(self, qquin, vaid):
        return requests.get(
            self.BASE_URL + self.USER_HOT_INFO_URL + '?qquin=' + qquin + '&vaid=' + vaid,
            headers=self.headers).json()

    def get_battle_summary_info(self, qquin, vaid):
        return requests.get(
            self.BASE_URL + self.BATTLT_SUMMARY_INFO + '?qquin=' + qquin + '&vaid=' + vaid,
            headers=self.headers).json()

    def get_champion(self):
        return requests.get(
            self.BASE_URL + self.CHAMPION,
            headers=self.headers).json()


# sha1加密
def to_sha1(part):
    sha1 = hashlib.sha1()
    sha1.update(part.encode())
    return sha1.hexdigest()


class WeixintranslateHandler(tornado.web.RequestHandler):
    # 验证开发账号
    @tornado.gen.coroutine
    def get(self):
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        token = "pyworm"
        list = [token, timestamp, nonce]
        list.sort()
        list = "".join(list)
        hashcode = to_sha1(list)
        if hashcode == signature:
            self.finish(echostr)

    # 对外接口
    @tornado.gen.coroutine
    def post(self):
        user = "o-r9yuIDvsCbLZ-dF-VpU3fVSxcs"
        master = "gh_4103522d4013"
        body = self.request.body
        data = ET.fromstring(body)
        content = data.find("Content").text
        msgType = data.find("MsgType").text
        FromUserName = data.find("FromUserName").text
        ToUserName = data.find("ToUserName").text
        CreateTime = int(time.time())
        if type(content).__name__ == "unicode":
            content = content.encode('UTF-8')
        if content == '杀的你喊妈彡':
            demo = Daiwan()
            word = demo.get_user_info(content)
            request_log.info(word)

            data = word['data'][0]
            level = data['level']
            name = data['name']
            area_id = data['area_id']
            win_point = data['win_point']
            icon_id = data['icon_id']
            tier = data['tier']
            qquin = data['qquin']
            queue = data['queue']

            name = 'name：{0}'.format(name)
            level = 'level：{0}'.format(level)
            area_id = 'area_id：{0}'.format(area_id)
            win_point = 'win_point：{0}'.format(win_point)
            icon_id = 'icon_id：{0}'.format(icon_id)
            tier = 'tier：{0}'.format(tier)
            qquin = 'qquin：{0}'.format(qquin)
            queue = 'queue：{0}'.format(queue)

            from PIL import Image, ImageDraw, ImageFont

            font = ImageFont.truetype('simsun.ttc', 24)
            # img = Image.new('RGB', (300, 200), (255, 255, 255))
            img = Image.open('/root/mazhen/pyworm-blog/pywormsite/static/lol/lol.png')
            draw = ImageDraw.Draw(img)
            draw.text((90, 30), name, (0, 0, 0), font=font)
            draw.text((90, 60), level, (0, 0, 0), font=font)
            draw.text((90, 90), area_id, (0, 0, 0), font=font)
            draw.text((90, 120), win_point, (0, 0, 0), font=font)
            draw.text((90, 150), icon_id, (0, 0, 0), font=font)
            draw.text((90, 180), tier, (0, 0, 0), font=font)
            draw.text((90, 210), qquin, (0, 0, 0), font=font)
            draw.text((90, 240), queue, (0, 0, 0), font=font)
            # draw.text((0, 60), unicode('你好', 'utf-8'), (0, 0, 0), font=font)
            img.save('/root/mazhen/pyworm-blog/pywormsite/static/lol/' + 'lol9.png')

            picurl = 'http://139.196.43.6/static/lol/lol9.png'

            data = '''
                <xml>
                 <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                 <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                 <CreateTime>{CreateTime}</CreateTime>
                 <MsgType><![CDATA[news]]></MsgType>
                 <ArticleCount>1</ArticleCount>
                 <Articles>
                 <item>
                 <Title><![CDATA['LOL']]></Title>
                 <Description><![CDATA['测试']]></Description>
                 <PicUrl><![CDATA[{picurl}]]></PicUrl>
                 <Url><![CDATA[{url}]]></Url>
                 </item>
                 </Articles>
                 </xml>
            '''
            resp = data.format(ToUserName=FromUserName, FromUserName=ToUserName,
                               CreateTime=CreateTime,
                               picurl=picurl, url=picurl)

            self.finish(resp)

        else:
            Content = youdao(content)

            data = '''
                <xml>
                    <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
                    <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
                    <CreateTime>{CreateTime}</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[{Content}]]></Content>
                </xml>
            '''

            # FromUserName, ToUserName需要互换
            resp = data.format(ToUserName=FromUserName, FromUserName=ToUserName,
                               CreateTime=CreateTime,
                               Content=Content)
            self.finish(resp)
