import datetime
import json
import xml.etree.ElementTree as ET
from http.cookiejar import CookieJar
from urllib import request
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor

from tornado.httpclient import HTTPClient, HTTPRequest


def get_weather():
    url = "http://api.map.baidu.com/telematics/v3/weather?location=%E5%8D%97%E4%BA%AC&output=XML&ak=FK9mkfdQsloEngodbFl4FeY3"
    http_client = HTTPClient()
    response = http_client.fetch(url, method="GET", request_timeout=120)
    response_body = response.body.decode()
    root = ET.fromstring(response_body)
    date = root.findall('results/weather_data/date')[1].text
    weather = root.findall('results/weather_data/weather')[1].text
    wind = root.findall('results/weather_data/wind')[1].text
    temperature = root.findall('results/weather_data/temperature')[1].text
    pm = root.find('results/pm25').text

    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)
    weather = str(
        tomorrow) + ' ' + date + ' ' + '南京' + ' ' + temperature + ' ' + weather + ' ' + wind + ' ' + 'PM2.5:' + pm
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
    bizuin=cookie_dict["bizuin"], data_bizuin=cookie_dict["data_bizuin"],
    data_ticket=cookie_dict["data_ticket"],
    slave_sid=cookie_dict["slave_sid"], slave_user=cookie_dict["slave_user"], )

# 保存消息
url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg?t=ajax-response&sub=update&type=10&token=840848985&lang=zh_CN"

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '1000',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': weixin_cookie or '',
    'Host': 'mp.weixin.qq.com',
    'Origin': 'https://mp.weixin.qq.com',
    'Pragma': 'no-cache',
    'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&lang=zh_CN&token=840848985&type=10&appmsgid=402861880&isMul=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

body = {
    'token': token,
    'lang': 'zh_CN',
    'f': 'json',
    'ajax': '1',
    'random': '0.8142554857768118',
    'AppMsgId': '402861880',
    'count': '1',
    'title0': '南京天气',
    'content0': '<p>' + get_weather() + '</p>',
    'digest0': get_weather(),
    'author0': '',
    'fileid0': '402861876',
    'music_id0': '',
    'video_id0': '',
    'show_cover_pic0': '0',
    'shortvideofileid0': '',
    'copyright_type0': '0',
    'can_reward0': '0',
    'reward_wording0': '',
    'need_open_comment0': '0',
    'sourceurl0': '',
    'free_content0': '',
    'fee0': '0',
}

body = urlencode(body)

http_client = HTTPClient()
request = HTTPRequest(url=url, method='POST', headers=headers, body=body)
response = http_client.fetch(request)
response_body = response.body.decode('utf8')
print("RESP:", response_body)
http_client.close()

# 发送消息
url = "https://mp.weixin.qq.com/cgi-bin/operate_appmsg?sub=preview&t=ajax-appmsg-preview&type=10&token={token}&lang=zh_CN".format(
    token=token)

headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Length': '3850',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': weixin_cookie or '',
    'Host': 'mp.weixin.qq.com',
    'Origin': 'https://mp.weixin.qq.com',
    'Pragma': 'no-cache',
    'Referer': 'https://mp.weixin.qq.com/cgi-bin/appmsg?t=media/appmsg_edit&action=edit&lang=zh_CN&token=840848985&type=10&appmsgid=402861880&isMul=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.107 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

body = {
    'token': token,
    'lang': 'zh_CN',
    'f': 'json',
    'ajax': '1',
    'random': '0.8142554857768118',
    'AppMsgId': '402861880',
    'count': '1',
    'title0': 'hello',
    'content0': '<p>' + get_weather() + '</p>',
    'digest0': get_weather(),
    'author0': '',
    'fileid0': '402861876',
    'music_id0': '',
    'video_id0': '',
    'show_cover_pic0': '0',
    'shortvideofileid0': '',
    'copyright_type0': '0',
    'can_reward0': '0',
    'reward_wording0': '',
    'need_open_comment0': '0',
    'sourceurl0': '',
    'free_content0': '',
    'fee0': '0',
    'preusername': 'ma373908',
    'imgcode': '',
    'is_preview': '1',
}
body = urlencode(body)

http_client = HTTPClient()
request = HTTPRequest(url=url, method='POST', headers=headers, body=body)
response = http_client.fetch(request)
response_body = response.body.decode('utf8')
print("RESP:", response_body)
http_client.close()
