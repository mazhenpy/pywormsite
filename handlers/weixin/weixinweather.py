from http.cookiejar import CookieJar
from urllib import request
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor
import json
import time
import xml.etree.ElementTree as ET

from tornado.httpclient import HTTPClient, HTTPRequest


def get_weather():
    url = "http://php.weather.sina.com.cn/xml.php?city=%C4%CF%BE%A9&password=DJOYnieT8234jlsK&day=1"
    http_client = HTTPClient()
    response = http_client.fetch(url, method="GET", request_timeout=120)
    response_body = response.body.decode()
    root = ET.fromstring(response_body)
    city = root.find('Weather/city').text
    status1 = root.find('Weather/status1').text
    status2 = root.find('Weather/status2').text
    temperature1 = root.find('Weather/temperature1').text
    temperature2 = root.find('Weather/temperature2').text
    savedate_weather = root.find('Weather/savedate_weather').text
    weather = savedate_weather + ' ' + city + ' ' + status1 + ' ' + status2 + ' ' + temperature2 + '-' + temperature1 + '°'
    print(weather)
    http_client.close()
    return weather


cookie = CookieJar()
opener = request.build_opener(HTTPCookieProcessor(cookie))

parse = {
    "username": "1053556056@qq.com",
    "pwd": "69eb5bac0eb7d5fa605e0954b858d026",
    "imgcode": "",
    "f": "json",
}

opener.addheaders = [
    ('Accept', '*/*'),
    ('Accept-Encoding', 'gzip, deflate'),
    ('Accept-Language', 'zh-CN,zh;q=0.8'),
    ('Cache-Control', 'no-cache'),
    ('Connection', 'keep-alive'),
    ('Content-Length', '81'),
    ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
    ('Host', 'mp.weixin.qq.com'),
    ('Origin', 'https://mp.weixin.qq.com'),
    ('Pragma', 'no-cache'),
    ('Referer', 'https://mp.weixin.qq.com/cgi-bin/loginpage'),
    ('User-Agent',
     'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36'),
    ('X-Requested-With', 'XMLHttpRequest'),
]

url = "https://mp.weixin.qq.com/cgi-bin/login"

request_data = urlencode(parse).encode('utf-8')

response = opener.open(url, request_data)

response_info = response.read().decode()
response_info = json.loads(response_info)
print('RESP:', response_info)

err_msg = response_info["base_resp"]["err_msg"]
print("Login status:", err_msg)

redirect_url = response_info["redirect_url"]
print("Redirect_url:", redirect_url)

token = redirect_url.split('token=')[1]
print("Token:", token)

cookie_dict = {}
print(cookie)

for c in cookie:
    if not cookie_dict.get(c.name):
        cookie_dict[c.name] = c.value

weixin_cookie = 'bizuin={bizuin};data_bizuin={data_bizuin};data_ticket={data_ticket};slave_sid={slave_sid};slave_user={slave_user}'.format(
    bizuin=cookie_dict["bizuin"], data_bizuin=cookie_dict["data_bizuin"], data_ticket=cookie_dict["data_ticket"],
    slave_sid=cookie_dict["slave_sid"], slave_user=cookie_dict["slave_user"], )

url = "https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&f=json&token={token}&lang=zh_CN".format(token=token)

headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Length': '156',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': weixin_cookie or '',
    'Host': 'mp.weixin.qq.com',
    'Origin': 'https://mp.weixin.qq.com',
    'Pragma': 'no-cache',
    'Referer': 'https://mp.weixin.qq.com/cgi-bin/singlesendpage?tofakeid=o-r9yuIDvsCbLZ-dF-VpU3fVSxcs&t=message/send&action=index&quickReplyId=402546325&token=1783210242&lang=zh_CN',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

body = {
    'token': token,
    'lang': 'zh_CN',
    'f': 'json',
    'ajax': '1',
    'random': '0.18187317857518792',
    'type': '1',
    'content': get_weather(),
    'tofakeid': 'o-r9yuIDvsCbLZ-dF-VpU3fVSxcs',
    'quickReplyId': str(int(time.time())),
    'imgcode': '',
}
body = urlencode(body)

http_client = HTTPClient()
request = HTTPRequest(url=url, method='POST', headers=headers, body=body)
response = http_client.fetch(request)
response_body = response.body.decode('utf8')
print("RESP:", response_body)
http_client.close()






