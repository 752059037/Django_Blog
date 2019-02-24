# -*- coding: utf-8 -*-
# Create your views here.

import json
from django import views
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views.decorators.csrf import csrf_exempt
from blog.models import Article, Category, Comment, UserInfo
from blog.forms import ArticleForm
from django.http import QueryDict
from hashlib import md5


def index(request):
    """
    博客首页
    :param request:
    :return:
    """
    article_list = Article.objects.all().order_by('-date_time')[0:5]
    return render(request, 'blog/index.html', {"article_list": article_list,
                                               "source_id": "index"})


def articles(request, pk):
    """
    博客列表页面
    :param request:
    :param pk:
    :return:
    """
    pk = int(pk)
    if pk:
        category_object = get_object_or_404(Category, pk=pk)
        category = category_object.name
        article_list = Article.objects.filter(category_id=pk)
    else:
        # pk为0时表示全部
        article_list = Article.objects.all()  # 获取全部文章
        category = u''
    return render(request, 'blog/articles.html', {"article_list": article_list,
                                                  "category": category,
                                                  })


def about(request):
    return render(request, 'blog/about.html')


def archive(request):
    article_list = Article.objects.order_by('-date_time')
    return render(request, 'blog/archive.html', {"article_list": article_list})


def link(request):
    return render(request, 'blog/link.html')


def message(request):
    return render(request, 'blog/message_board.html', {"source_id": "message"})


@csrf_exempt
def getComment(request):
    """
    接收畅言的评论回推， post方式回推
    :param request:
    :return:
    """
    arg = request.POST
    data = arg.get('data')
    data = json.loads(data)
    title = data.get('title')
    url = data.get('url')
    source_id = data.get('sourceid')
    if source_id not in ['message']:
        article = Article.objects.get(pk=source_id)
        article.commenced()
    comments = data.get('comments')[0]
    content = comments.get('content')
    user = comments.get('user').get('nickname')
    Comment(title=title, source_id=source_id, user_name=user, url=url, comment=content).save()
    return JsonResponse({"status": "ok"})


def detail(request, pk):
    """
    博文详情
    :param request:
    :param pk:
    :return:
    """
    article = get_object_or_404(Article, pk=pk)
    article.viewed()
    return render(request, 'blog/detail.html', {"article": article,
                                                "source_id": article.id})


def search(request):
    """
    搜索
    :param request:
    :return:
    """
    key = request.GET.get('key')
    print(request)
    article_list = Article.objects.filter(title__icontains=key)
    return render(request, 'blog/search.html',
                  {"article_list": article_list, "key": key})


def tag(request, name):
    """
    标签
    :param request:
    :param name
    :return:
    """
    article_list = Article.objects.filter(tag__tag_name=name)
    return render(request, 'blog/tag.html', {"article_list": article_list,
                                             "tag": name})


def game(request, id):
    """
    标签
    :param request:
    :param name
    :return:
    """
    print('id: ', id)
    return render(request, 'game/game1.html')


def addblog(request):
    form_obj = ArticleForm()
    
    return render(request, 'blog/addblog.html', {'form_obj': form_obj})


def alt_blog(request, pk):
    print(pk)
    form_obj = ArticleForm()
    
    return render(request, 'blog/addblog.html', {'form_obj': form_obj})


def next_url(request):
    """
    一个返回原来页面的函数
    :param request:
    :return:
    """
    obj = QueryDict(mutable=True)  # 跳转回编辑之前的URL操作
    obj['next_url'] = request.get_full_path()  # 生成一个Query对象 然后在对象里添加url
    next_url = obj.urlencode()  # 利用QueryDict的urlencode 将nexturl编码
    return next_url


class Add_Blog(views.View):  # 添加/编辑文章二合一
    @staticmethod
    def get(request, pk):
        _id = pk
        print(_id)
        customer_obj = Article.objects.filter(id=_id).first()
        form_obj = ArticleForm(instance=customer_obj)
        return render(request, 'blog/addblog.html', {'form_obj': form_obj, 'id': _id})
    
    @staticmethod
    def post(request, pk):
        _id = pk
        article_obj = Article.objects.filter(id=_id).first()
        form_obj = ArticleForm(request.POST, instance=article_obj)
        if form_obj.is_valid():
            form_obj.save()
            _next_url = reverse('blog:article', kwargs={'pk': 0})
            return redirect(_next_url)
        return render(request, 'blog/addblog.html', {'form_obj': form_obj, 'id': _id})


class Login(views.View):
    
    def get(self, request):
        return render(request, 'blog/login.html')
    
    def post(self, request):
        # 1.获取用户输入
        username = request.POST.get('username')
        pswd = request.POST.get('password')
        # 2.检测用户密码是否正确
        user_obj = UserInfo.objects.filter(username=username, password=pswd).first()
        if user_obj:  # 登陆成功
            # 保存session并回写Cookie
            md5_obj = md5()
            md5_obj.update(bytes(username + pswd, encoding='utf-8'))  # 对用户信息进行加密
            MD5_COOKIE = md5_obj.hexdigest()  # 拿到加密字符串
            request.session['session'] = MD5_COOKIE
            if request.POST.get('is_check'):
                request.session.set_expiry(7 * 24 * 60 * 60)
            return redirect(reverse('index'))
        else:
            return render(request, 'blog/login.html', {'error_msg': '账号或密码错误'})
