from django.forms import Form
from django.forms import widgets
from django.forms import fields
from app01 import models
from bs4 import BeautifulSoup
from utils.XssFilter import xss

class RegisterForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={"class":"form-control"})
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={"class":"form-control"})
    )


    password1 = fields.CharField(
        widget=widgets.PasswordInput(attrs={"class":"form-control"})
    )


    nickname = fields.CharField(
        widget=widgets.TextInput(attrs={"class":"form-control"})
    )

    email = fields.EmailField(
        widget=widgets.TextInput(attrs={"class": "form-control"})
    )

    check_str = fields.CharField(
        widget=widgets.TextInput(attrs={"class":"form-control"})
    )

    # 上传头像的路径
    avatar = fields.FileField(
        widget=widgets.FileInput(attrs={"id":"img2"})
    )


    def __init__(self, request=None, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.request = request

    def clean_check_str(self):
        """
        验证码判决
        :return:
        """
        check_str1 = self.cleaned_data["check_str"]
        be_checked_str = self.request.session.get("check_str")
        if check_str1.upper() == be_checked_str.upper():
            return check_str1
        from django.core.exceptions import ValidationError
        raise ValidationError("验证码输入错误")

    def clean(self):
        """
        判断注册时密码输入
        :return:
        """
        from django.core.exceptions import ValidationError
        cleaned_data = super(RegisterForm, self).clean()
        pwd = cleaned_data.get("password")
        pwd1 = cleaned_data.get("password1")
        if pwd != pwd1:
            # raise ValidationError("密码输入不一致")
            self.add_error("password1","密码输入不一致")



class AddArticleForm(Form):
    """

    """
    def __init__(self,blog_obj=None,*args, **kwargs):
        super(AddArticleForm, self).__init__(*args, **kwargs)
        self.blog_obj = blog_obj
        # 为Category_id动态传入选项
        self.fields["category_id"].widget.choices = models.Category.objects.filter(blog=self.blog_obj).\
            values_list("nid", "title")
        # 动态传入tag标签
        self.fields["tag_id"].choices = models.Tag.objects.filter(blog=self.blog_obj).\
            values_list("nid", "title")



    title = fields.CharField(
        widget=widgets.TextInput(attrs={"class":"form-control"})
    )

    article_type_id = fields.IntegerField(
        widget=widgets.Select(choices=models.Article.type_choices)
    )

    category_id = fields.IntegerField(
        widget=widgets.Select()
    )

    # tag_id = fields.MultipleChoiceField(
    #     widget=widgets.SelectMultiple
    # )
    tag_id = fields.MultipleChoiceField(widget=widgets.CheckboxSelectMultiple())

    content = fields.CharField(
        widget=widgets.Textarea(attrs={"id":"i1"})
    )

    def clean_content(self):
        """
        防范xss攻击，过滤关键字
        :return:
        """
        old = self.cleaned_data["content"]
        return xss(old)





