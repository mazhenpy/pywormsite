# coding:utf-8
import json
import datetime
import logging

from django.shortcuts import render_to_response
from django import forms
from django.template import RequestContext
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from forum.models import Post, Replay, Post14, Replay14


request_log = logging.getLogger('request')
access_log = logging.getLogger('access')


#定义发布博客表单类型
class PostForm(forms.Form):
    title = forms.CharField(label='标题:', max_length=30)
    content = forms.CharField(label='内容:', widget=forms.Textarea)


#定义评论表单类型
class ReplayForm(forms.Form):
    content = forms.CharField(label='内容:', widget=forms.Textarea)


#定义注册表单类型
class RegisterForm(forms.Form):
    usernm = forms.CharField(label='用户名:', max_length=30)
    passwd = forms.CharField(label='密码:', widget=forms.PasswordInput())
    passwd2 = forms.CharField(label='再次输入:', widget=forms.PasswordInput())

    def pwd_validate(self, p1, p2):
        return p1 == p2


#定义登录表单类型
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名:', max_length=30, widget=forms.TextInput(attrs={'': '', }))
    password = forms.CharField(label='密码:', widget=forms.PasswordInput())


#发表帖子
@csrf_exempt
def post_add(req):
    form1 = LoginForm(req.POST)
    form2 = RegisterForm(req.POST)
    errors = []
    if req.method == "POST":
        form = PostForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data['title']
            content = data['content']
            if title:
                post = Post()
                post.title = title
                post.content = content
                post.post_time = datetime.datetime.today()
                post.post_user = req.COOKIES.get('username', '')
                post.save()
                form = PostForm()
            else:
                errors.append('温馨提示：请输入标题！')
    else:
        form = PostForm()  #如果表填的不对刷新重来
    #先执行这里
    posts = Post.objects.all()
    num = len(posts)
    username = req.COOKIES.get('username', '')
    form1 = LoginForm(req.POST)
    form2 = RegisterForm(req.POST)
    return render_to_response('blogs.html', {
        'posts': posts,
        'form': form,
        'form1': form1,
        'form2': form2,
        'num': num,
        'errors': errors,
        'username': username,
    }, context_instance=RequestContext(req))


#发表帖子
@csrf_exempt
def post_add2(request):
    form = PostForm(request.POST)
    form1 = LoginForm(request.POST)
    form2 = RegisterForm(request.POST)
    if request.is_ajax():
        title = request.POST.get("title", None)
        content = request.POST.get("content", None)
        if True:
            post = Post()
            post.title = title
            post.content = content
            post.post_time = datetime.datetime.today()
            post.post_user = request.COOKIES.get('username', '')
            post.save()
            form = PostForm()
    posts = Post.objects.all()
    num = len(posts)
    username = request.COOKIES.get('username', '')
    form1 = LoginForm(request.POST)
    form2 = RegisterForm(request.POST)
    return render_to_response('blogs.html', {
        'posts': posts,
        'form': form,
        'form1': form1,
        'form2': form2,
        'num': num,
        'username': username,
    }, context_instance=RequestContext(request))


#多对一关系对帖子评论
@csrf_exempt
def replays(req, post_id):
    print(">>>>>>",post_id)
    blog = Post.objects.get(id=post_id)
    blog.read_num += 1
    blog.save()

    form = None
    if req.is_ajax():
        content = req.POST.get('content', None)
        if content:
            item = Post.objects.get(id=post_id)
            Replay.objects.create(content=content, post=item, replay_time=datetime.datetime.today(),
                                  replay_user=req.COOKIES.get('username', ''))  #将评论写进数据库
            return HttpResponse(json.dumps({"content": content}))
    else:
        form = ReplayForm()

    post_id = post_id
    replays = Post.objects.get(id=post_id).replay_set.all()  #一条帖子的所有评论
    num = int(len(replays))
    title = Post.objects.get(id=post_id).title
    content = Post.objects.get(id=post_id).content
    username = req.COOKIES.get('username', '')
    ip = req.META.get('REMOTE_ADDR', '0.0.0.0')
    return render_to_response('blogs.html', {
        'content': content,
        'post_id': post_id,
        'num': num,
        'title': title,
        'replays': replays,
        'username': username,
        'form': form,
        'ip': ip,
    }, context_instance=RequestContext(req))


#发表小说
@csrf_exempt
def post_add14(req, parent_id):
    form = PostForm(req.POST)
    form1 = LoginForm(req.POST)
    form2 = RegisterForm(req.POST)
    errors = []
    if req.method == "POST":
        form = PostForm(req.POST)
        if form.is_valid():
            data = form.cleaned_data
            title = data['title']
            content = data['content']
            if title:
                post = Post14()
                post.parent_id = parent_id
                post.title = title
                post.content = content
                post.post_time = datetime.datetime.today()
                post.post_user = req.COOKIES.get('username', '')
                post.save()
                form = PostForm()
            else:
                errors.append('温馨提示：请输入标题！')
    else:
        form = PostForm()  #如果表填的不对刷新重来

    posts = Post14.objects.filter(parent_id=parent_id)
    num = len(posts)
    username = req.COOKIES.get('username', '')
    form1 = LoginForm(req.POST)
    form2 = RegisterForm(req.POST)
    return render_to_response('blogs.html', {
        'posts': posts,
        'form': form,
        'form1': form1,
        'form2': form2,
        'num': num,
        'errors': errors,
        'username': username,
    }, context_instance=RequestContext(req))


#多对一关系对小说评论
@csrf_exempt
def replays14(req, post_id):
    blog = Post14.objects.get(id=post_id)
    blog.read_num += 1
    blog.save()

    form = None
    if req.is_ajax():
        content = req.POST.get('content', None)
        if content:
            item = Post14.objects.get(id=post_id)
            Replay14.objects.create(content=content, post=item, replay_time=datetime.datetime.today(),
                                    replay_user=req.COOKIES.get('username', ''))  #将评论写进数据库
            return HttpResponse(json.dumps({"content": content}))
    else:
        form = ReplayForm()
    post_id = post_id

    replays = Post14.objects.get(id=post_id).replay14_set.all()  #一条帖子的所有评论
    num = int(len(replays))
    title = Post14.objects.get(id=post_id).title
    content = Post14.objects.get(id=post_id).content
    username = req.COOKIES.get('username', '')
    ip = req.META.get('REMOTE_ADDR', '0.0.0.0')
    return render_to_response('blogs.html', {
        'content': content,
        'post_id': post_id,
        'num': num,
        'title': title,
        'replays': replays,
        'username': username,
        'form': form,
        'ip': ip,
    }, context_instance=RequestContext(req))


#    if req.method == "POST":
#                form = ReplayForm(req.POST)
#                if form.is_valid():
#                        data = form.cleaned_data
#                        content = data['content']
#                        p=Post.objects.get(id=post_id)      
#                        Replay.objects.create(content=content,post=p)#将评论写进数据库
#    else:
#            form = ReplayForm()
#    num = int(Post.objects.get(id=post_id).read_num)
#    replays = Post.objects.get(id=post_id).replay_set.all()#一条帖子的所有评论
#    title = Post.objects.get(id=post_id).title
#    content = Post.objects.get(id=post_id).content
#    return render_to_response('blogs.html',{'replays':replays,'title':title,'content':content,'num':num},context_instance=RequestContext(req))





@csrf_exempt
def blog_post(req, post_id):
    blog = Post.objects.get(id=post_id)
    blog.read_num += 1
    blog.save()

    form = None
    if req.is_ajax():
        content = req.POST.get('content', None)
        if content:
            item = Post.objects.get(id=post_id)
            Replay.objects.create(content=content, post=item, replay_time=datetime.datetime.today(),
                                  replay_user=req.COOKIES.get('username', ''))
            return HttpResponse(json.dumps({"content": content}))
    else:
        form = ReplayForm()
    post_id = post_id
    replays = Post.objects.get(id=post_id).replay_set.all()
    num = int(len(replays))
    content = Post.objects.get(id=post_id).content
    username = req.COOKIES.get('username', '')
    return render_to_response('blogs.html', {
        'content': content,
        'post_id': post_id,
        'num': num,
        'replays': replays,
        'username': username,
        'form': form,
    }, context_instance=RequestContext(req))

