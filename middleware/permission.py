from django.middleware.csrf import CsrfViewMiddleware
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse


class PermissionMiddle(MiddlewareMixin):
    """
    权限过滤,中间件
    """

    def process_request(self, request, *args, **kwargs):

        # 只有授权才能访问的url
        invalid_url = ["/permit/order.html"]

        if request.path_info in invalid_url:
            action = request.GET.get("md")  # GET传参---?md=get
            permission_dic = request.session.get("permission_dict")
            # {
            #   '/order.html': ['post', 'get', 'edit', 'del'],
            #   '/users.html': ['post', 'get', 'edit', 'del']
            # }
            if not permission_dic:
                return HttpResponse("无权限（未登录）")

            action_list = permission_dic.get(request.path_info)
            if not action_list:
                return HttpResponse("无权限2")

            if action not in action_list:
                return HttpResponse("无权限3")


