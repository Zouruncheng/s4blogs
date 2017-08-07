from django.shortcuts import render,redirect,HttpResponse
from app01 import models,forms
import json
import os

def myadmin(request,*args,**kwargs):

    login_info = request.session.get("login_info")
    if not login_info:
        return redirect("/login/")

    # kwargs={'category_id': 1, 'tags__nid': 1, 'article_type_id': 1}
    condition = {}
    for k, v in kwargs.items():
        kwargs[k] = int(v)
        if v != "0":
            condition[k] = int(v)

    user_obj = models.Userinfo.objects.filter(nid=login_info["nid"]).first()
    blog_obj = models.Blog.objects.filter(user_id=login_info["nid"]).first()

    condition["blog_id"] = blog_obj.nid


    article_type_list = models.Article.type_choices

    category_list = models.Category.objects.filter(blog=blog_obj).all()

    tag_list = models.Tag.objects.filter(blog=blog_obj).all()

    # 获取文章对象
    article_list = models.Article.objects.filter(**condition).all()

    return render(request, "myadmin.html", {"article_type_list":article_type_list,
                                            "category_list":category_list,
                                            "tag_list":tag_list,
                                            "kwargs": kwargs,
                                            "article_list":article_list,
                                            "user_obj":user_obj,
                                            "blog_obj":blog_obj})


CONTENT=""
def add_article(request):

    login_info = request.session.get("login_info")
    if not login_info:
        return redirect("/login")
    # 传入博客对象到form组件
    blog_obj = models.Blog.objects.filter(user_id=login_info["nid"]).first()
    if request.method == "GET":
        # 生成form组件
        obj = forms.AddArticleForm(blog_obj)
        return render(request, "add_article.html",{"obj":obj})
    else:
        obj = forms.AddArticleForm(blog_obj,request.POST)
        if not obj.is_valid():
            return render(request, "add_article.html", {"obj": obj})
        # print(obj.cleaned_data)

        tag_id = obj.cleaned_data.pop("tag_id")      # 取出文章的标签
        content = obj.cleaned_data.pop("content")    # 取出文章的内容
        obj.cleaned_data["summary"] = content[0:100]  # 切割文章内容，保存在article表中，summary字段中
        obj.cleaned_data["blog_id"] = blog_obj.nid
        # print(obj.cleaned_data)

        from django.db import transaction
        with transaction.atomic():
            # 插入article表
            new_article_obj = models.Article.objects.create(**obj.cleaned_data)
            # 插入article_detail表
            # print(content)
            models.ArticleDetail.objects.create(content=content,article_id=new_article_obj.nid)
            # 插入article2tag表
            for item in tag_id:
                models.Article2Tag.objects.create(article_id=new_article_obj.nid, tag_id=item)



            # tag_list = models.Tag.objects.filter(nid__in=tag_id).all()
            # article_id = [new_article_obj.nid for i in tag_id]
            # print(article_id)
            # condition = dict(list(zip(article_id, tag_id)))
            # print(condition)
            # models.Article2Tag.objects.create(**condition)

        return HttpResponse("发布成功靓仔")





def see(request):
    return render(request,"see.html", {"con": CONTENT})





def upload_img(request):
    """
    kindEditor上传头像
    :param request:
    :return: 上传头像只能返回特定格式的数据。
    """
    f = request.FILES.get("imgFile")
    path = os.path.join("static/avatar",f.name)
    # print(path)
    with open(path, "wb+") as file:
        for chunk in f.chunks():
            file.write(chunk)

    # kindEditor只能返回特定格式的数据
    dic = {
        'error': 0,
        'url': '/' + path,
        'message': '错误了...'
    }

    return HttpResponse(json.dumps(dic))




def del_article(request):

    response = {"status":True,"msg":None}
    try:
        article_id = request.POST.get("article_id")
        print(article_id)






    return HttpResponse("okay")