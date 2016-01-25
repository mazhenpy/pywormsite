# coding:utf-8
import json
import datetime
import re
import logging
import os
from xmlrpc.server import SimpleXMLRPCDispatcher

from bs4 import BeautifulSoup
from django.core.cache import cache
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from tornado.httpclient import HTTPClient
import yaml

from blog.models import Blog, Replay, IP_access
from pywormsite import RedisDriver


request_log = logging.getLogger('request')
error_log = logging.getLogger('error')


# 博客展示
@csrf_exempt
def blog(req, blog_id):
    ip = ''
    if 'HTTP_X_FORWARDED_FOR' in req.META:
        ip = req.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = req.META['REMOTE_ADDR']

    ip_attribution = sina_ip(ip)

    ips_access = cache.get("ips_access_{0}".format(blog_id), [])
    if ip not in ips_access:
        ips_access.append(ip)
        if len(ips_access) > 5:
            ips_access.pop(0)
        cache.set("ips_access_{0}".format(blog_id), ips_access, 60 * 60 * 24 * 30)


    master_14 = RedisDriver().master_14
    ips_info = {}
    ips_access = cache.get("ips_access_{0}".format(blog_id), [])
    if ips_access:
        for ip in ips_access:
            ip_access_time = master_14.get(ip)
            ips_info[ip_attribution] = ip_access_time

    ip_obj = IP_access.objects.filter(ip=ip)
    blog_obj = Blog.objects.filter(blog_id=blog_id)

    ip_num = 0
    if blog_obj:
        blog = Blog.objects.get(blog_id=blog_id)
        if ip_obj:  #如果已存在此ip
            ip = IP_access.objects.get(ip=ip)
            ip.blogs.add(blog)
            ip_num = blog.ip_access_set.all()
            blog.IP_num = len(ip_num)
            blog.PV_num += 1
            blog.save()
        else:
            ip = IP_access(ip=ip)
            ip.save()
            ip.blogs.add(blog)
            ip_num = blog.ip_access_set.all()
            blog.IP_num = len(ip_num)
            blog.PV_num += 1
            blog.save()

    #print(len(ip_num))

    if req.method == "POST":
        content = req.POST.get('content', None)
        p_id = req.POST.get('p_id', None)
        if p_id and content:
            blog = Blog.objects.get(blog_id=blog_id)

            Replay.objects.create(content=content, blog=blog, replay_time=datetime.datetime.today(),
                                  replay_user=ip_attribution, replay_id=0, parent_id=p_id)

            return HttpResponse(json.dumps({"content": content}))

        elif content:
            item = Blog.objects.get(blog_id=blog_id)
            num = 0
            try:
                blog = Blog.objects.get(blog_id=blog_id)
                replays_re = Replay.objects.filter(blog=blog, replay_id=0)
                replays_er = Replay.objects.filter(blog=blog)
                replays = int(len(replays_er)) - (len(replays_re))
                num = replays
            except Exception as e:
                error_log.error(e)

            Replay.objects.create(content=content, blog=item, replay_time=datetime.datetime.today(), replay_user=ip_attribution,
                                  replay_id=num + 1, parent_id=0)
            return HttpResponse(json.dumps({"content": content}))

    blog_id = blog_id
    replays = None
    replay_num = None
    PV_num = None
    to_replays_dict = {}
    blog_list = []
    try:
        # replays = Blog.objects.get(blog_id=blog_id).replay_set.all()
        blog = Blog.objects.get(blog_id=blog_id)
        categorie = blog.categorie
        PV_num = blog.PV_num
        replays = Replay.objects.filter(blog=blog, parent_id=0)
        replay_num = int(len(replays))  # 评论数量
        for replay in replays:
            to_replays = Replay.objects.filter(blog=blog, parent_id=replay.id)
            to_replays_dict[replay] = to_replays

    except Exception as e:
        error_log.error(e)
    return render_to_response(blog_id + '.html', {
        'blog_id': blog_id,
        'replay_num': replay_num,
        'PV_num': PV_num,
        'ip_num': ip_num,
        'replays': replays,
        'to_replays_dict': to_replays_dict,
        'ips_info':ips_info
    }, context_instance=RequestContext(req))


# 获取IP归属地
def sina_ip(ip):
    attribution = ""
    if ip == "127.0.0.1":
        ip = '183.208.22.171'
    http_client = HTTPClient()
    response = None
    url = "http://int.dpool.sina.com.cn/iplookup/iplookup.php?format=js&ip={0}".format(ip)
    try:
        response = http_client.fetch(url, method='GET', request_timeout=120)
    except Exception as e:
        request_log.info(e)
    finally:
        http_client.close()

    if response and response.code == 200:
        response_body = eval(response.body.decode('utf8')[21:-1])
        try:
            province = response_body['province']
            city = response_body['city']
            attribution = city  #+province
        except Exception as e:
            error_log.error(e)

    ip_piece = ip.split(".")
    ip_piece[1] = '*'
    ip_piece[2] = '*'
    ip_attribution = '网友' + '.'.join(ip_piece) + '[' + attribution + ']'

    return ip_attribution


#web开发
def web(req):
    blogs = None
    num = None
    page_num_list = []
    try:
        blogs = Blog.objects.filter(categorie='Web开发')
        num = len(blogs)
        paginator = Paginator(blogs, 10)
        try:
            page = int(req.GET.get('page', 1))
            blogs = paginator.page(page)
            for i in range(blogs.paginator.num_pages):
                page_num_list.append(i + 1)

        except (EmptyPage, InvalidPage, PageNotAnInteger):
            blogs = paginator.page(1)
    except Exception as e:
        error_log.error(e)
    return render_to_response('blogs.html', {
        'blogs': blogs,
        'num': num,
        'page_num_list': page_num_list,
        'categorie': 'Web开发'
    }, RequestContext(req))


#网络爬虫
def spider(req):
    blogs = None
    num = None
    page_num_list = []
    try:
        blogs = Blog.objects.filter(categorie='网络爬虫')
        num = len(blogs)
        paginator = Paginator(blogs, 10)
        try:
            page = int(req.GET.get('page', 1))
            blogs = paginator.page(page)
            for i in range(blogs.paginator.num_pages):
                page_num_list.append(i + 1)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            blogs = paginator.page(1)
    except Exception as e:
        error_log.error(e)
    return render_to_response('blogs.html', {
        'blogs': blogs,
        'num': num,
        'page_num_list': page_num_list,
        'categorie': '网络爬虫'
    }, RequestContext(req))


#Tornado
def tornado(req):
    blogs = None
    num = None
    page_num_list = []
    try:
        blogs = Blog.objects.filter(categorie='Tornado')
        num = len(blogs)
        paginator = Paginator(blogs, 10)
        try:
            page = int(req.GET.get('page', 1))
            blogs = paginator.page(page)
            for i in range(blogs.paginator.num_pages):
                page_num_list.append(i + 1)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            blogs = paginator.page(1)
    except Exception as e:
        error_log.error(e)
    username = req.COOKIES.get('username', '')
    return render_to_response('blogs.html', {
        'username': username,
        'blogs': blogs,
        'num': num,
        'page_num_list': page_num_list,
        'categorie': 'Tornado'
    }, RequestContext(req))


#Python编程
def python(req):
    blogs = None
    num = None
    page_num_list = []
    try:
        blogs = Blog.objects.filter(categorie='Python编程')
        num = len(blogs)
        paginator = Paginator(blogs, 10)
        try:
            page = int(req.GET.get('page', 1))
            blogs = paginator.page(page)
            for i in range(blogs.paginator.num_pages):
                page_num_list.append(i + 1)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            blogs = paginator.page(1)
    except Exception as e:
        error_log.error(e)
    return render_to_response('blogs.html', {
        'blogs': blogs,
        'num': num,
        'page_num_list': page_num_list,
        'categorie': 'Python编程'
    }, RequestContext(req))


#Notes
def notes(req):
    blogs = None
    num = None
    page_num_list = []
    try:
        blogs = Blog.objects.filter(categorie='网络爬虫')  #Notes
        num = len(blogs)
        paginator = Paginator(blogs, 10)
        try:
            page = int(req.GET.get('page', 1))
            blogs = paginator.page(page)
            for i in range(blogs.paginator.num_pages):
                page_num_list.append(i + 1)
        except (EmptyPage, InvalidPage, PageNotAnInteger):
            blogs = paginator.page(1)
    except Exception as e:
        error_log.error(e)
    return render_to_response('notes.html', {
        'blogs': blogs,
        'num': num,
        'page_num_list': page_num_list,
        'categorie': '网络爬虫'
    }, RequestContext(req))


# 网站地图
def catalog(req):
    blogs = None
    try:
        blogs = Blog.objects.all()
    except Exception as e:
        error_log.error(e)
    return render_to_response('catalog.html', {'blogs': blogs}, RequestContext(req))


#更新数据库
def to_mysql(req):
    path = r'{0}/templates'.format(os.path.dirname(__file__))
    num = len(sum([i[2] for i in os.walk(path)], [])) - 1
    id = 1
    for i in range(num):
        url = "{0}/templates/{1}.html".format(os.path.dirname(__file__), id)
        #url = "blog/templates/1.html"
        try:
            soup = BeautifulSoup(open(url, encoding="UTF-8"))
            if len(soup):
                categorie = soup.find(id='categorie').string
                blog_id = id
                title = soup.find(id='blog_title').string
                post_time = str(soup.find(id='blog_post_time'))[35:45]

                blog = Blog()
                blog.blog_id = blog_id
                blog.title = title
                blog.post_time = post_time
                blog.categorie = categorie
                blog.save()
            else:
                break
        except Exception as e:
            error_log.error(e)
        finally:
            id += 1
    return HttpResponse("<div style='text-align:center;'>{0} - To-Mysql-Done</div>".format(id))


#生成静态页面
def static(id, win_content, categorie, title):
    print("博客id", id)
    try:
        context = {
            "win_content": win_content,
            "categorie": categorie,
            "title": title,
            "post_time": datetime.datetime.today()
        }
        static_html = '{0}/templates/{1}.html'.format(os.path.dirname(__file__), id)
        #if not os.path.exists(static_html):
        if True:
            base_path = '{0}/templates/0.html'.format(os.path.dirname(__file__))
            content = render_to_string(base_path, context)

            with open(static_html, 'w', encoding='UTF-8') as static_file:
                static_file.write(content)
                #print("静态文件已生成:", id)
    except Exception as e:
        error_log.error(e)


#测试配置文件
def test(req):
    config = yaml.load(
        open(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/config.yaml', 'r', encoding='utf8'))
    id = config["win_live_writer"]["id"]
    return HttpResponse(id)


#获取文章摘要
def get_summary(text, count, suffix=u''):
    summary = re.sub(r'<.*?>', u'', text)
    summary = summary[0:count]
    return u'{0}{1}'.format(summary, suffix)


#MetaWeblog 接口API
class Api(object):
    #博客的信息
    def getUsersBlogs(self, appkey, username, password):
        self.__isUser(username, password)

        struct = {}
        try:
            config = yaml.load(open(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/config.yaml', 'r',
                                    encoding='utf8'))
            struct['blogid'] = config["win_live_writer"]["blogid"]
            struct['url'] = config["win_live_writer"]["url"]
            struct['blogName'] = config["win_live_writer"]["blogName"]
        except Exception as e:
            error_log.error(e)


        tmp = []
        tmp.append(struct)
        return tmp

    #返回基于字典的文章对应//最近发布
    def getPost(self, postid, username, password):
        self.__isUser(username, password)
        # print("客户端请求博客ID:", postid)
        config = yaml.load(
            open(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/config.yaml', 'r', encoding='utf8'))

        blog = Blog.objects.get(blog_id=postid)
        struct = {}
        struct['postid'] = postid
        struct['title'] = blog.title
        #struct['description'] = blog.content
        struct['description'] = "XXXXXXXXXXXXXXXXXXXX"  #测试
        struct['link'] = config["win_live_writer"]["url"] + '/blog/' + postid
        # print(blog.content)
        # print(struct)
        return struct

    #返回最近基于字典的文章对应
    def getRecentPosts(self, blogid, username, password, numberOfPosts=5):
        self.__isUser(username, password)
        print("ffffffffffff")
        blogs = Blog.objects.all()
        tmp = []
        for blog in blogs:
            struct = {}
            struct['postid'] = blog.blog_id
            struct['title'] = blog.title
            struct['description'] = blog.content
            tmp.append(struct)
        return tmp

    #发布新的博客
    def newPost(self, blogid, username, password, struct, publish):
        self.__isUser(username, password)
        # print(("blogid:", blogid))
        # print(("struct:", struct))

        title = struct['title']
        content = struct['description']
        categorie = struct['categories'][0]

        #生成静态HTML文件
        id = None
        try:
            path = r'{0}/templates'.format(os.path.dirname(__file__))
            id = len(sum([i[2] for i in os.walk(path)], []))
            # print("博客ID：", id)
            static(id, content, categorie, title)

            blog = Blog()
            blog.blog_id = id
            blog.title = title
            blog.categorie = categorie
            blog.content = content
            blog.summary = get_summary(content, 150, u'...')
            blog.post_time = datetime.datetime.today()
            blog.save()

        except Exception as e:
            error_log.error("生成静态文件失败:{0}".format(e))

        return id

    #编辑对应的博客
    def editPost(self, postid, username, password, struct, publish):
        self.__isUser(username, password)
        # print("postid:", postid)
        # print("struct:", struct)
        title = struct['title']
        content = struct['description']
        categorie = struct['categories'][0]
        # print("categorie:", categorie)

        static(postid, content, categorie, title)

        blog = Blog.objects.get(blog_id=postid)
        blog.title = title
        blog.content = content
        blog.categorie = categorie
        blog.save()
        return True


    #获取分类目录
    def getCategories(self, blogid, username, password):
        self.__isUser(username, password)

        struct1 = {}
        struct1['categoryId'] = 1
        struct1['categoryName'] = 'Python编程'
        # struct['htmlUrl'] = 'localhost/categroy/1'
        # struct['rssUrl'] = 'localhost/categroy/1'
        struct2 = {}
        struct2['categoryId'] = 2
        struct2['categoryName'] = '网络爬虫'
        struct3 = {}
        struct3['categoryId'] = 3
        struct3['categoryName'] = 'Web开发'
        struct4 = {}
        struct4['categoryId'] = 4
        struct4['categoryName'] = 'Tornado'
        struct5 = {}
        struct5['categoryId'] = 5
        struct5['categoryName'] = 'Notes'
        tmp = []
        tmp.append(struct1)
        tmp.append(struct2)
        tmp.append(struct3)
        tmp.append(struct4)
        tmp.append(struct5)
        return tmp

    #上传图片
    def newMediaObject(self, blogid, username, password, data):
        self.__isUser(username, password)

        name = data['name']
        type = data['type']
        bits = data['bits']

        (basename, filename) = os.path.split(name)
        print(basename,filename)
        img_path = os.path.pardir + os.path.join('/static/image/blog', filename)
        print("img_path:", img_path)

        if not os.path.exists(os.path.pardir + '/static/image/blog'):
            os.makedirs(os.path.pardir + '/static/image/blog')

        if not os.path.isfile(img_path):
            file_i = open(img_path, 'wb')
            file_i.write(bits.data)
            file_i.close()

        struct = {}
        struct['url'] = '/' + (img_path)
        # print("struct_url:", struct['url'])
        return struct

    #删除博客
    def deletePost(self, appkey, postid, username, password, publish):
        self.__isUser(username, password)
        return True

    #验证用户名密码
    def __isUser(self, username, password):
        username=None
        password=None
        try:
            config = yaml.load(open(os.path.abspath(os.path.dirname(os.path.dirname(__file__))) + '/config.yaml', 'r',
                                    encoding='utf8'))
            username = config["win_live_writer"]["username"]
            password = config["win_live_writer"]["password"]
        except Exception as e:
            error_log.error(e)
        if not (username == username and password == password):
            #raise xmlrpclib.Fault(401, '用户名或密码错误！')
            return HttpResponse(401, '用户名或密码错误！')



#使用windows live writer发布博客
@csrf_exempt
def metaweblog(request):
    request_log.info("目标请求:{0}".format(request.body))

    dispatcher = SimpleXMLRPCDispatcher(allow_none=False, encoding="UTF-8")
    dispatcher.register_introspection_functions()
    dispatcher.register_function(Api().getUsersBlogs, 'blogger.getUsersBlogs')
    dispatcher.register_function(Api().getCategories, 'metaWeblog.getCategories')
    dispatcher.register_function(Api().getRecentPosts, 'metaWeblog.getRecentPosts')
    dispatcher.register_function(Api().getPost, 'metaWeblog.getPost')
    dispatcher.register_function(Api().newPost, 'metaWeblog.newPost')
    dispatcher.register_function(Api().newMediaObject, 'metaWeblog.newMediaObject')
    dispatcher.register_function(Api().editPost, 'metaWeblog.editPost')
    dispatcher.register_function(Api().deletePost, 'metaWeblog.deletePost')

    response = dispatcher._marshaled_dispatch(request.body)
    request_log.info("响应目标:{0}".format(response))
    return HttpResponse(response)

    # def wlwmanifest(req):
    #     return render_to_response('wlwmanifest.xml')