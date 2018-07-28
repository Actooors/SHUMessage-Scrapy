import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib

import re


agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
header = {
    "Host": "www.sz.shu.edu.cn",
    "Referer": "http://www.sz.shu.edu.cn/Login.aspx?ReturnUrl=http://www.sz.shu.edu.cn/index.aspx",
    "User-Agent": agent
}
session = requests.session()

"""
将cookie保存到本地
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
"""

"""
将得到cookies加载到session中
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print("cookie未能加载")
"""

def shuzhi_login(username,password):
    #孰知网登录
    print("一卡通登录")
    post_url = "http://www.sz.shu.edu.cn/api/Sys/Users/Login"
    post_data = {
        "username": username,
        "password": password
    }

    response_text = session.post(post_url, data=post_data, headers=header)

    #session.cookies.save()#将cookie保存到本地

def get_status():
    #通过个人主页具有当未登录时状态编码为302重定向的特性来判断用户是否已经登录
    status_url = "http://www.sz.shu.edu.cn/people/personinfo.aspx" #孰知网个人主页url
    response = session.get(status_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True

shuzhi_login("16121666","Xw52655384")
get_status()
