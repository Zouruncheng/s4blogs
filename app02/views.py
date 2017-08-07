import re
from django.shortcuts import render,redirect,HttpResponse
from app02 import models




def permit(request):
    """
    权限管理，获取权限，并存放在session中
    :param request:
    :return:
    """
    from django.db.models import Count

    user_obj = models.User.objects.filter(username="zouruncheng").first()
    print(user_obj)

    # 获取 user2role信息
    x = models.User2Role.objects.filter(user_id=user_obj.id)


    # 通过users关联到User2Role表，通过user__关联到user表。获取当前用户的角色
    role_obj = models.Role.objects.filter(users__user__username="zouruncheng").all()
    print(role_obj)

    # 一个用户可能有多个角色，查询出的数据可能重复。annotate分组问题？
    # permission_list = models.Permission2Action2Role.objects.filter(role__in=role_obj).\
    #     values("permission__url","action__code").annotate(c=Count("id"))

    # 使用distinct时效率较低，不会增加额外的列
    permission_list = models.Permission2Action2Role.objects.filter(role__in=role_obj).\
        values("permission__url","action__code").distinct()

    print(permission_list)

    # 构造权限条件
    permission_dict = {}
    for item in permission_list:
        if item["permission__url"] in permission_dict:
            permission_dict[item["permission__url"]].append(item["action__code"])
        else:
            permission_dict[item["permission__url"]]=[item["action__code"]]
    print(permission_dict)
    # {'/order.html': ['post', 'get', 'edit', 'del'], '/users.html': ['post', 'get', 'edit', 'del']}

    request.session["permission_dict"] = permission_dict
    return HttpResponse("模拟登录成功")


def show(request):
    return HttpResponse("登录，且有权限。才能看见我")


# ==========================day90===============================================
# 根据表结构，生成权限菜单
def menu(request):
    all_menu_list = models.Menu.objects.values("id", "caption", "parent_id")
    # print(all_menu_list)

    # user = models.User.objects.filter(rusername="zouruncheng")
    role_list = models.Role.objects.filter(users__user__username="zouruncheng").all()
    permission_list = models.Permission2Action2Role.objects.filter(role__in=role_list).\
        values("permission__id", "permission__url", "permission__caption", "permission__menu__id").distinct()
    # print(permission_list)
    # print(permission_list.count())

    # 将权限挂靠到菜单上
    all_menu_dict = {}
    for row in all_menu_list:
        row["child"] = []
        row["status"] = False  # 是否显示该权限
        row["opened"] = False  # 菜单是否展开
        all_menu_dict[row["id"]]=row

    for per in permission_list:
        if not per["permission__menu__id"]:
            continue

        item = {
            "id":per["permission__id"],
            "caption":per["permission__caption"],
            "url":per["permission__url"],
            "parent_id":per["permission__menu__id"],
            "status":True,
            "opened":False
        }

        # if re.match("permission__url",request.path_info):
        if re.match(item["url"], "/permit/users.html"):
            item["opened"]=True

        pid = item["parent_id"]

        all_menu_dict[pid]["child"].append(item)

        # 将当前权限的父级status=True
        temp = pid
        while not all_menu_dict[temp]["status"]:
            all_menu_dict[temp]["status"]=True
            temp = all_menu_dict[temp]["parent_id"]
            if not temp:
                break

        # 将当前权限的父级opened = True
        if item["opened"]:
            temp1 = pid
            while not all_menu_dict[temp1]["opened"]:
                all_menu_dict[temp1]["opened"] = True
                temp1 = all_menu_dict[temp1]["parent_id"]
                if not temp1:
                    break

    # print(all_menu_dict)
    # print(all_menu_list)
    # 构造菜单和菜单之间的等级关系
    result=[]
    for row in all_menu_list:
        if row["parent_id"]:
            all_menu_dict[row["parent_id"]]["child"].append(row)
        else:
            result.append(row)
    # print(result)

    # for row in result:
    #     print("----",row["caption"],row["status"],row["opened"])
        """
        ---- 用户管理 True
        ---- 订单管理 True
        ---- 博客管理 False
        """
        '''
        结构化处理结果
        result= [
            {'id':1, 'caption':'菜单1', parent_id:None,status:True,opened:True,child:[

                    {'url':'/order.html','caption': '订单管理','id': 1,'opened': True, 'status': True},
                    {'id':4, 'caption':'菜单1-1', parent_id:1,status:False,opened:False,child:[]},]},

            {'id':2, 'caption':'菜单2', parent_id:None,status:True,opened:False,child:[]},

            {'id':3, 'caption':'菜单3', parent_id:None,status:False,opened:False,child:[]},

        ]
        '''
    def menu_tree(menu_list):
        tpl1 = """
        <div class='menu-item'>
            <div class='menu-header'>{0}</div>
            <div class='menu-body {2}'>{1}</div>
        </div>
        """
        tpl2 = """
        <a href='{0}' class='{1}'>{2}</a>
        """

        menu_str = ""
        for menu in menu_list:
            if not menu['status']:
                continue
            # menu: 菜单，权限（url）
            if menu.get('url'):
                # 权限
                menu_str += tpl2.format(menu['url'],'active' if menu['opened'] else "",menu['caption'])
            else:
                # 菜单
                if menu['child']:
                    child_html = menu_tree(menu['child'])
                else:
                    child_html = ""
                menu_str += tpl1.format(menu['caption'], child_html,"" if menu['opened'] else 'hide')

        return menu_str

    menu_html = menu_tree(result)
    print(menu_html)
    return render(request,"ShowMenu.html",{"menu_html":menu_html})

















