from django.shortcuts import render, HttpResponse, redirect
import os
import json
from app01 import models
from utils.pager import PageInfo


def index(request):
    type_choice_list = models.Article.type_choices
    # print(type_choice_list)
    return render(request, "index.html", {"type_choice_list": type_choice_list,
                                          })


def index1(request, *args, **kwargs):
    login_info = request.session.get("login_info")
    # print(login_info)
    # print(request.path_info)
    # print(args,kwargs)
    type_id = int(kwargs.get("type_id")) if kwargs.get("type_id") else None
    # print(type_id)
    type_choice_list = models.Article.type_choices
    # print(type_choice_list)
    return render(request, "index1.html", {"type_choice_list": type_choice_list,
                                           "type_id": type_id,
                                           "login_info": login_info})


from django.forms import Form
from django.forms import widgets
from django.forms import fields


class LoginForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={"class": "form-control"})
    )

    check_str = fields.CharField(
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )


def login(request):
    if request.method == "GET":
        obj = LoginForm()
        return render(request, "login.html", {"obj": obj})
    else:
        obj = LoginForm(request.POST)
        if obj.is_valid():
            # session获取随机字符串
            check_str = request.session.get("check_str")
            be_checked_str = obj.cleaned_data.pop("check_str")

            if not check_str == be_checked_str:
                # 如果验证码输入不正确
                return render(request, "login.html", {"obj": obj,
                                                      "str_error": "验证码错误"})

            obj = models.Userinfo.objects.filter(**obj.cleaned_data).first()
            if obj:
                # print(obj.avatar)
                # 在session中传入登录信息
                request.session["login_info"] = {"status": True,
                                                 "user": obj.username,
                                                 "nid":obj.nid,
                                                 "avatar": str(obj.avatar)}

            # 跳转到上次的url
            current_path = request.session.get("current_path")
            if current_path:
                return redirect(current_path)
            return redirect("/")
        return render(request, "login.html", {"obj": obj,
                                              "user_error": "用户名或密码错误"})

def logout(request):
    current_path = request.session.get("current_path")
    request.session.delete(request.session.session_key)
    if not current_path:
        return redirect("/")
    return redirect(current_path)




from app01.forms import RegisterForm


def register1(request):
    if request.method == "GET":
        obj = RegisterForm()
        return render(request, "register1.html", {"obj": obj})
    else:
        obj = RegisterForm(request, request.POST, request.FILES)
        if not obj.is_valid():
            return render(request, "register1.html", {"obj": obj})

        # 获取输入头像,写入到static目录
        file_obj = obj.cleaned_data["avatar"]
        file_path = os.path.join("static/avatar", file_obj.name)
        # print(file_path)
        with open(file_path, "wb") as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        # 从数据中删除验证码
        obj.cleaned_data.pop("check_str")
        obj.cleaned_data.pop("password1")
        # 把头像对象换成路径
        obj.cleaned_data["avatar"] = "/" + file_path
        # 插入数据到数据库
        print(obj.cleaned_data)
        models.Userinfo.objects.create(**obj.cleaned_data)
        return redirect("/")


def upload(request):
    """
    上传头像
    :param request:
    :return:
    """
    if request.method == "POST":
        file_obj = request.FILES.get("fafafa")
        file_path = os.path.join("static/avatar", file_obj.name)
        # print(file_path)
        with open(file_path, "wb") as f:
            for chunk in file_obj.chunks():
                f.write(chunk)
        return HttpResponse(file_path)


from django.db.models import Count


def home(request, *args, **kwargs):
    # 获取站点信息
    site = kwargs.get("site")

    # 获取当前blog对象
    blog_obj = models.Blog.objects.filter(site=site).first()
    if not blog_obj:
        return redirect("/")

    # 获取当前site的userinfo对象
    user_obj = models.Userinfo.objects.filter(blog=blog_obj).first()

    # 获取category列表
    # category_list = models.Category.objects.filter(blog=blog_obj).all()
    category_list = models.Article.objects.filter(blog=blog_obj).values("category__nid", "category__title").annotate(
        ccount=Count("nid"))

    # 获取tag列表
    tag_list = models.Article2Tag.objects.filter(tag__blog=blog_obj).values("tag__nid", "tag__title").annotate(
        tcount=Count("nid"))

    # 获取datetime列表
    date_list = models.Article.objects.filter(blog=blog_obj).extra(
        select={"ctime": "date_format(create_time,'%%Y-%%m')"}).values("ctime").annotate(c=Count("nid"))
    # print(date_list)date_list


    # 获取登录的session
    login_info = request.session.get("login_info")


    # 分页对象
    current_page = request.GET.get("page")
    all_count = models.Article.objects.filter(blog=blog_obj).all().count()
    base_url = "/home/%s" % (site)
    page_obj = PageInfo(current_page, all_count, 8, base_url)

    # 获取article列表
    article_obj = models.Article.objects.filter(blog=blog_obj).all()[page_obj.start():page_obj.end()]

    # 为当前url设置session
    request.session["current_path"] = request.path_info

    return render(request, "home.html", {"blog_obj": blog_obj,
                                         "user_obj": user_obj,
                                         "category_list": category_list,
                                         "tag_list": tag_list,
                                         "date_list": date_list,
                                         "article_obj": article_obj,
                                         "obj": page_obj,
                                         "login_info":login_info})


def detail(request, **kwargs):
    site = kwargs.get("site")
    nid = kwargs.get("nid")
    blog_obj = models.Blog.objects.filter(site=site).first()

    # 获取用户信息
    user_obj = models.Userinfo.objects.filter(blog__site=site).first()
    # 获取文章对象
    article_obj = models.Article.objects.filter(nid=nid).first()
    category_list = models.Article.objects.filter(blog=blog_obj).values("category__nid", "category__title").annotate(
        ccount=Count("nid"))

    # 获取tag列表
    tag_list = models.Article2Tag.objects.filter(tag__blog=blog_obj).values("tag__nid", "tag__title").annotate(
        tcount=Count("nid"))

    # 获取datetime列表
    date_list = models.Article.objects.filter(blog=blog_obj).extra(
        select={"ctime": "date_format(create_time,'%%Y-%%m')"}).values("ctime").annotate(c=Count("nid"))
    # print(date_list)date_list

    # 获取文章细节
    article_detail = models.ArticleDetail.objects.filter(article_id=nid).first()

    # 为当前url设置session
    # print(request.path_info)
    # request.session.set_expiry(15)
    request.session["current_path"] = request.path_info

    # 获取登录的session
    login_info = request.session.get("login_info")

    # 点赞
    # like_count = models.UpDown.objects.filter(article_id=nid, up=1).all().count()
    # dislike_count = models.UpDown.objects.filter(article_id=nid,up=0).all().count()

    # 评论
    # comment_list = models.Comment.objects.filter(article_id=nid).\
    #     values("nid","user__nid","user__avatar","create_time","user__nickname","reply__nid","content").order_by("create_time")
    # print(comment_list)
    # comment_dic= {}
    # for row in comment_list:
    #     row["child"]=[]
    #     comment_dic[row["nid"]]=row
    #
    #
    # new_comment_list = []
    # for item in comment_list:
    #     if item["reply__nid"]:
    #         comment_dic[item["reply__nid"]]["child"].append(item)
    #     else:
    #         new_comment_list.append(item)
    # print(new_comment_list)

    # 后端生成html标签
    # from utils.multicomment import comment_tree
    # comment_str = comment_tree(new_comment_list)









    return render(request, "home_article.html", {"user_obj": user_obj,
                                                 "blog_obj": blog_obj,
                                                 "category_list": category_list,
                                                 "tag_list": tag_list,
                                                 "date_list": date_list,
                                                 "article_obj": article_obj,
                                                 "article_detail": article_detail,
                                                 "login_info":login_info})


def filter(request, *args, **kwargs):
    site = kwargs.get("site")
    condition = kwargs.get("condition")
    nid = kwargs.get("nid")
    # 获取site博客对象
    blog_obj = models.Blog.objects.filter(site=site).first()

    user_obj = models.Userinfo.objects.filter(blog=blog_obj).first()

    # 获取category_list
    category_list = models.Article.objects.filter(blog=blog_obj). \
        values("category__nid", "category__title").annotate(ccount=Count("nid")).all()

    # 获取taglist
    tag_list = models.Article2Tag.objects.filter(tag__blog=blog_obj). \
        values("tag__nid", "tag__title").annotate(tcount=Count("nid")).all()

    # 获取date_list
    date_list = models.Article.objects.filter(blog=blog_obj). \
        extra(select={"ctime": "date_format(create_time,'%%Y-%%m')"}). \
        values("ctime").annotate(c=Count("nid")).all()

    # 分页对象
    # 获取all_count不同url下所有书籍
    if condition == "category":
        all_count = models.Article.objects.filter(blog=blog_obj, category__nid=nid).all().count()
    elif condition == "tag":
        all_count = models.Article.objects.filter(blog=blog_obj, tags__nid=nid).all().count()
    elif condition == "date":
        all_count= article_obj = models.Article.objects.filter(blog=blog_obj). \
            extra(where=["date_format(create_time,'%%Y-%%m')=%s"], params=[nid, ]).all().count()
    # 获取当前页
    current_page = request.GET.get("page")
    base_url = "/home/%s/%s/%s.html" % (site, condition, nid)
    page_obj = PageInfo(current_page, all_count, 8, base_url)

    # 获取site+blog.site对象
    if condition == "category":
        article_obj = models.Article.objects.filter(blog=blog_obj, category__nid=nid).all()[
            page_obj.start(): page_obj.end()]

    elif condition == "tag":
        article_obj = models.Article.objects.filter(blog=blog_obj, tags__nid=nid).all()[
            page_obj.start():page_obj.end()]

    elif condition == "date":
        article_obj = models.Article.objects.filter(blog=blog_obj). \
            extra(where=["date_format(create_time,'%%Y-%%m')=%s"], params=[nid, ]).all()[
            page_obj.start():page_obj.end()]

    # 为当前url设置session
    request.session["current_path"] = request.path_info

    # 获取登录的session
    login_info = request.session.get("login_info")


    return render(request, "home.html", {"blog_obj": blog_obj,
                                         "user_obj": user_obj,
                                         "category_list": category_list,
                                         "tag_list": tag_list,
                                         "date_list": date_list,
                                         "obj": page_obj,
                                         "article_obj": article_obj,
                                         "login_info":login_info})

import re
from django.db.models import F,Q
def updown(request):
    # 获取点赞类型
    up = request.POST.get("up")

    # 用正则切割获取文章id
    article_id = request.POST.get("article_id")
    article_id = re.search("\d+",article_id).group()

    # 获取登录session
    login_info = request.session.get("login_info")
    if not login_info:
        return HttpResponse("请先登录再搞事情")

    # 获取是否点赞
    updown_obj = models.UpDown.objects.filter(up=up,article_id=article_id,user_id=login_info["nid"]).first()
    if updown_obj:
        if up == "1":
            return HttpResponse("你已经赞过了")
        return HttpResponse("你已经踩过了")

    # 事物
    from django.db import transaction
    # with transaction.atomic()：

    # 在数据库中插入点赞信息
    obj = models.UpDown.objects.create(up=up,article_id=article_id,user_id=login_info["nid"])
    if up == "1":
        models.Article.objects.filter(nid=article_id).update(up_count=F("up_count")+1)
    elif up == "0":
        models.Article.objects.filter(nid=article_id).update(down_count=F("down_count")+1)

    return HttpResponse("ok")


def comment(request):
    nid = request.POST.get("nid")
    print(nid)
    comment_list = models.Comment.objects.filter(article_id=nid).\
        values("nid","user__nid","user__avatar","user__nickname","reply__nid","content").order_by("create_time")

    # 构造评论字典
    comment_dic= {}
    for row in comment_list:
        row["child"]=[]
        comment_dic[row["nid"]]=row

    # 返回新的评论列表
    new_comment_list = []
    for item in comment_list:
        if item["reply__nid"]:
            comment_dic[item["reply__nid"]]["child"].append(item)
        else:
            new_comment_list.append(item)

    return HttpResponse(json.dumps(new_comment_list))



def put_comment(request):
    # 获取用户session
    login_info = request.session.get("login_info")
    if not login_info:
        return HttpResponse("你个瓜娃子，请先登录")

    article_id = request.POST.get("article_id")
    article_id = re.search("\d+",article_id).group()
    content = request.POST.get("content")
    # print(article_id, content, login_info["nid"])
    models.Comment.objects.create(user_id=login_info["nid"],article_id=article_id,content=content)

    return HttpResponse("okay")


# 验证码功能
def check_code(request):
    # f = open("static/1.jpg","rb")
    # data = f.read()
    # f.close()
    # return HttpResponse(data)

    # from PIL import Image
    # f = open("2.jpg", "wb")
    # img = Image.new(mode="RGB", size=(120,30), color=(0,255,0))
    # img.save(f, "png")
    # f.close()

    # from PIL import Image,ImageDraw,ImageFont
    # 创建一张图片对象
    # img = Image.new(mode="RGB", size=(120, 30), color=(0,255,0))

    # 创建一个画笔对象
    # draw = ImageDraw.Draw(img, mode="RGB")

    # 生成随机字符串
    # check_str = "".join([chr(random.randint(65,90)) for i in range(5)])

    # 写入随机字符串
    # draw.text([0,0], check_str, "black",)

    # 存储到文件
    # f = open("2.png", "wb")
    # img.save(f, "png")
    # f.close()
    # return HttpResponse(f1.read)

    # 存储到内存
    # from io import BytesIO
    # f1 = BytesIO()
    # img.save(f1, "png")
    # return HttpResponse(f1.getvalue())


    # f1 = open("2.png", "rb")
    # data = f1.read()
    # f1.close()
    # img = Image.new(mode="RGB", size=(120, 30), color=(0,255,0))
    # draw = ImageDraw.Draw(img, mode="RGB")

    # char_list=[]
    # for i in range(5):
    #     char = chr(random.randint(65,90))
    #     draw.text([i*24,0], char, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
    # f = open("2.png", "wb")
    # img.save(f, "png")
    # f.close()
    #
    # f1 = open("2.png", "rb")
    # data = f1.read()
    # f1.close()

    from io import BytesIO
    from utils import random_check_code
    img, check_str = random_check_code.check_code(120, 30, 5, "utils/domi.ttf", 28)
    stream = BytesIO()
    img.save(stream, "png")
    request.session["check_str"] = check_str
    return HttpResponse(stream.getvalue())
