# coding:utf-8
import logging
import time
import datetime
from django.core.cache import cache
from django.shortcuts import render_to_response, RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User  # ,Permission
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from blog.views import sina_ip
from purus.models import Access_amount_mon, Access_amount_day, Access_ip


request_log = logging.getLogger('request')
error_log = logging.getLogger('error')
access_log = logging.getLogger('access')

# 网站首页
@csrf_exempt
@cache_page(60 * 15) #缓存页面15分钟
def index(req):
    if req.is_ajax():
        username = req.POST.get("username", None)
        password = req.POST.get("password", None)
        if login_validate(req, username, password):
            response = render_to_response('index.html', RequestContext(req))
            response.set_cookie('username', username, 3600)
            return response

    online_num = 0
    ips_all = cache.get("ips_all", [])
    if ips_all:
        online_ip_dict = cache.get_many(ips_all).keys()
        online_num = len(online_ip_dict)

    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
    access_day = cache.get(day, {'IP': 0, 'PV': 0})
    access_yesterday = cache.get(yesterday, {'IP': 0, 'PV': 0})

    access_day_ip = access_day["IP"]
    access_day_pv = access_day["PV"]
    access_yesterday_ip = access_yesterday["IP"]
    access_yesterday_pv = access_yesterday["PV"]

    return render_to_response('index.html', {
        'online_num': online_num,
        'access_day_ip': access_day_ip,
        'access_day_pv': access_day_pv,
        'access_yesterday_ip': access_yesterday_ip,
        'access_yesterday_pv': access_yesterday_pv,
    }, RequestContext(req))

# visitor = json.loads(urllib2.urlopen(url+ip).read())
# province = visitor['province']
# city = visitor['city']
# 关于这里
# @cache_page(60 * 15) #缓存页面15分钟
def about(req):
    ips_info = {}
    ips_attribution = []
    ips_access = cache.get("ips_access", [])
    if ips_access:
        for ip in ips_access:
            ip_attribution = sina_ip(ip)
            ip_access_time = cache.get(ip,'')
            ips_info[ip_attribution] = ip_access_time

    return render_to_response('about_new.html', {"ips_info": ips_info}, RequestContext(req))


#后台管理
def admin(req):
    return HttpResponseRedirect('/admin/', RequestContext(req))


#网站收藏
@cache_page(60 * 15) #缓存页面15分钟
def collection(req):
    return render_to_response('my_collection.html', context_instance=RequestContext(req))


#movie
@cache_page(60 * 15) #缓存页面15分钟
def warcraft(req):
    return render_to_response('warcraft.html', context_instance=RequestContext(req))


#music
@cache_page(60 * 15) #缓存页面15分钟
def music(req):
    return render_to_response('music_rain.html', context_instance=RequestContext(req))


#判断用户名是否在数据库中
def login_validate(request, username, password):
    req_value = False
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return True
    return req_value


#将月访问量同步数据库
def access_count_mon(req):
    mon = time.strftime('%Y-%m', time.localtime(time.time()))
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
    yestermon = yesterday[:7]
    #同步上月
    access_count = cache.get(yestermon, {'IP': 0, 'PV': 0})

    item = Access_amount_mon()
    item.access_time = yestermon
    item.access_ip = access_count['IP']
    item.access_pv = access_count['PV']
    item.save()

    access_log.info("上月访问量-IP:{0}-PV:{1}".format(access_count['IP'],access_count['PV']))
    return HttpResponse("上月访问量-IP:{0}-PV:{1}".format(access_count['IP'],access_count['PV']))


#将日访问量同步数据库
def access_count_day(req):
    day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
    #同步昨日的
    access_count = cache.get(yesterday, {'IP': 0, 'PV': 0})

    item = Access_amount_day()
    item.access_time = yesterday
    item.access_ip = access_count['IP']
    item.access_pv = access_count['PV']
    item.save()

    access_log.info("{0}访问量-IP:{1}-PV:{2}".format(yesterday,access_count['IP'],access_count['PV']))
    return HttpResponse("{0}访问量-IP:{1}-PV:{2}".format(yesterday,access_count['IP'],access_count['PV']))


#将IP归属地同步数据库
def ips_to_sql(req):
    ips_to_sql = cache.get("ips_to_sql", [])
    num=0
    if ips_to_sql:
        for ip in ips_to_sql:
            ips_to_sql.remove(ip)
            cache.set("ips_to_sql", ips_to_sql)
            ip_attribution = sina_ip(ip)[-3:-1]
            item = Access_ip()
            item.ip = ip
            item.ip_attribution = ip_attribution
            item.save()
            num+=1

    access_log.info("{0}-IP-TO_MYSQL".format(num))
    return HttpResponse("{0}-IP-TO_MYSQL".format(num))


#当前在线人数
def online_ips(req):
    online_num = 0
    ips_all = cache.get("ips_all", [])
    if ips_all:
        online_ip_dict = cache.get_many(ips_all).keys()
        online_num = len(online_ip_dict)

    return HttpResponse(online_num)

#ajax验证账号密码
@csrf_exempt
def ajax_login(request):
    errors = ""
    username = request.POST.get("username", None)
    password = request.POST.get("password", None)
    if not password:
        errors = '<a>请输入密码</a>'
    elif not login_validate(request, username, password):
        errors = '<a>账号或密码错误</a>'
    return HttpResponse(errors, RequestContext(request))


#注册账号
@csrf_exempt
def regist(request):
    if request.is_ajax():
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = User.objects.create_user(username=username, password=password)
        user.is_staff = True
        user.save()
        return HttpResponse()

#检查账号信息
@csrf_exempt
def ajax_regist(request):
    errors=""
    username = request.POST.get("username",None)
    password = request.POST.get("password",None)
    password2= request.POST.get("password2",None)
    if User.objects.all().filter(username=username):
        errors = '<a>用户名已存在</a>'
    elif not password:
        errors = '<a>请输入密码</a>'
    elif not password2:
        errors = '<a>请输入密码</a>'
    else:
        errors = ''
    return  HttpResponse(errors,RequestContext(request))


#注销账号
def logout(req):
    auth_logout(req)
    response = HttpResponseRedirect('/index/')
    response.delete_cookie('username')
    return response


#ajax验证登录
@csrf_exempt
def ajax_login_username(req):
    rtxt = ""
    username = req.POST.get("username", None)
    #if username:
    #        if User.objects.filter(username=username):
    #                 rtxt='<img src="../static/image/ok.gif">'
    #        else:
    #                 rtxt='<img src="../static/image/nook.gif">'
    return HttpResponse(rtxt)

    #  返回json模式
    #  return  HttpResponse(json.dumps({'msg':rtxt}))
    #  text.(data.msg)


#ajax验证注册
@csrf_exempt
def ajax_register_username(req):
    rtxt = ""
    username = req.POST.get("username", None)
    #if username:
    #
    #        if User.objects.filter(username=username):
    #
    #                 rtxt='<img src="../static/image/nook.gif">'
    #        else:
    #                 rtxt='<img src="../static/image/ok.gif">'
    return HttpResponse(rtxt)


@csrf_exempt
def ajax_register_password(req):
    rtxt = ""
    password = req.POST.get("password", None)
    #if password:
    #                 rtxt='<img src="../static/image/ok.gif">'
    #else:
    #                 rtxt='<img src="../static/image/nook.gif">'
    return HttpResponse(rtxt)


@csrf_exempt
def ajax_register_password2(req):
    rtxt = ""
    password = req.POST.get("password", None)
    password2 = req.POST.get("password2", None)
    #if int(password2) == int(password):
    #                 rtxt='<img src="../static/image/ok.gif">'
    #else:
    #                 rtxt='<img src="../static/image/nook.gif">'
    return HttpResponse(rtxt)


@csrf_exempt
def jsimg(req):
    return render_to_response('js_img.html', RequestContext(req))


@csrf_exempt
def ajax_jsimg(req):
    rtxt = '<img src="http://www.pyworm.com/static/image/jqxx.jpg">'

    return HttpResponse(rtxt)




