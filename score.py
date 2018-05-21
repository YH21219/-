# -*- coding:UTF-8 -*-
import requests
import re
import time
import config
from pyquery import PyQuery as py

__author__ = '刘远航'
__date__ = '2018.5.10'
"""
模拟登录教务处
爬取成绩
"""


def log(*args,**kwargs):
    print(*args,**kwargs)

# 模拟登录
s = requests.session()
# requests库的session对象能够帮我们跨请求保持某些参数，也会在同一个session实例发出的所有请求之间保持cookies。
# 目标网站
URL = 'https://cas.dgut.edu.cn/home/Oauth/getToken/appid/jwxt.html'


# get redirect link
def get_redirect_url():
    res = s.get(URL, headers=config.header)
    req = re.compile(r'<script>.*?var.*?token.*?"(.*?)".*?</script>',
                     re.S)  # get token
    items = re.findall(req, res.text)
    username = input("please input username:")
    password = input("please input password:")
    token = items[0]
    data = {'username': username, 'password': password, '__token__': token}
    response = s.post(
        URL, headers=config.header, allow_redirects=False, data=data)
    if response.status_code != 200:
        return None
    log(response.text)
    log("login successful")
    req1 = re.compile(r'.*?token=(.*?)\\', re.S)
    items1 = re.findall(req1, response.text)
    log(items1[0])
    token = items1[0]
    direct_url = 'http://jwxt.dgut.edu.cn/dglgjw/login?token=' + token
    log("new link", direct_url)
    return direct_url


# login
def login():
    direct_url = get_redirect_url()
    try:
        response1 = s.get(direct_url, headers=config.header1)
        response1.encoding = 'gb2312'
    except Exception:
        log("异常捕捉")
    time.sleep(2)  # sleep 2S

# get score html
def get_html():
    url = 'http://jwxt.dgut.edu.cn/dglgjw/student/xscj.stuckcj_data.jsp'
    response_score = s.post(
        url, headers=config.header_show, data=config.form_data)
    html = response_score.text
    return html

def get_score(html):
    score = []
    doc = py(html)
    sco = doc('td')
    for i in sco.items():
        score.append(str(i.text()).split())
    # for i in score:
    #     log(i[0])
    return score

def parse_socre(score):
    title = score[:10]
    del score[:10]
    serial_number = []
    course = []
    credit = []
    category = []
    study_nature = []
    inspection_way = []
    get_way = []
    Score = []
    note  = []
    for i in score[::9]:
        serial_number.append(",".join(i))
    for i in score[1::9]:
        course.append(",".join(i))
    for i in score[2::9]:
        credit.append(",".join(i))
    for i in score[3::9]:
        category.append(",".join(i))
    for i in score[4::9]:
        study_nature.append(",".join(i))
    for i in score[5::9]:
        inspection_way.append(",".join(i))
    for i in score[6::9]:
        get_way.append(",".join(i))
    for i in score[7::9]:
        Score.append(",".join(i))
    for i in score[8::9]:
        note.append(",".join(i))
    
    return serial_number,course,credit,category,study_nature,inspection_way,get_way,Score,note


    
# logout user
def logout():
    url1 = 'http://jwxt.dgut.edu.cn/dglgjw/DoLogoutServlet'
    try:
        response3 = s.get(url1, headers=config.headers)
        print(response3.status_code)
        print("logout success")
    except Exception:
        print("异常")


# def sort_score(list_score):
#     del list_score[0]#去除第一个
#     del list_score[8]#去除备注
#     log('before',list_score)
#     title = list_score[:8]
#     log(title)
#     list_score = list_score[8:]
#     log('after',list_score)
    

#     return title,serial_number,course,credit,category,study_nature,inspection_way,get_way,score



if __name__ == '__main__':
    login()
    html = get_html()
    score = get_score(html)
    Tuple = parse_socre(score)
    log(Tuple)
    logout()
