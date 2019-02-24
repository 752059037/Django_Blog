# 创建人;WanChun Ye
# 创建时间 : 19.2.21  21:46


from django.utils.deprecation import MiddlewareMixin
import re
from django.shortcuts import redirect, reverse
from hashlib import md5
from blog.models import UserInfo


# 根据用户名和密码的MD5值做cookie


class RBAC(MiddlewareMixin):
    @staticmethod
    def process_request(request):
        # 判断当前这次请求的URL在不在权限列表里
        url = request.path_info  # 获取当前的url
        # print('当前URL:',url)
        user_obj = UserInfo.objects.all().first()
        username = user_obj.username
        password = user_obj.password
        md5_obj = md5()
        md5_obj.update(bytes(username + password, encoding='utf-8'))  # 对用户信息进行加密
        MD5_COOKIE = md5_obj.hexdigest()  # 拿到加密字符串
        _session = request.session.get('session')
        if _session == MD5_COOKIE:
            return
        # 做正则式 去匹配URL
        ret = re.findall(r'addblog/', url)
        ret2 = re.findall(r'alt_blog/', url)
        if ret or ret2:
            print('正则匹配到内容')
            return redirect(reverse('blog:login'))
        
        return  # 正则匹配不上放行

