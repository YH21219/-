import requests, re, time, openpyxl
from bs4 import BeautifulSoup
import config

__author__ = '刘远航'
__date__ = '2018.5.10'

"""
模拟登录教务处
爬取成绩
"""


# 代替print输出
def log(*args, **kw):
    print (*args, **kw)


# 模拟登录
s = requests.session ()
# requests库的session对象能够帮我们跨请求保持某些参数，也会在同一个session实例发出的所有请求之间保持cookies。
# 目标网站
URL = 'https://cas.dgut.edu.cn/home/Oauth/getToken/appid/jwxt.html'


# get redirect link
def get_redirect_url():
    res = s.get (URL, headers=config.header)
    req = re.compile (r'<script>.*?var.*?token.*?"(.*?)".*?</script>', re.S)  # get token
    items = re.findall (req, res.text)
    username = input ("please input username:")
    password = input ("please input password:")
    token = items[0]
    data = {'username': username, 'password': password, '__token__': token}
    response = s.post (URL, headers=config.header, allow_redirects=False, data=data)
    if response.status_code != 200:
        return None
    log (response.text)
    log ("login successful")
    req1 = re.compile (r'.*?token=(.*?)\\', re.S)
    items1 = re.findall (req1, response.text)
    log (items1[0])
    token = items1[0]
    direct_url = 'http://jwxt.dgut.edu.cn/dglgjw/login?token=' + token
    log ("new link", direct_url)
    return direct_url


def get_html():
    url = 'http://jwxt.dgut.edu.cn/dglgjw/student/xscj.stuckcj_data.jsp'
    response_score = s.post (url, headers=config.header_show, data=config.form_data)
    html = response_score.text
    return html


#  combination each list
def combination_list():
    list11 = []
    for i in range (0, len (list_nature)):
        list11.append ((list_number[i], list_get_course_name[i], list_credit[i], list_category[i], list_nature[i],
                        list_Assessment[i], list_mode[i], list_socer[i]))

    return list11


# write to excel
def wirte_file(path):
    liss = combination_list ()
    wb = openpyxl.Workbook ()
    sheet = wb.active
    sheet.title = 'score table'
    for i in range (0, len (list_nature)):
        for j in range (0, 8):
            sheet.cell (row=i + 1, column=j + 1, value=str (liss[i][j]))
    wb.save (path)
    log ("write success")


# get number
def get_number():
    list_number1 = []
    for i in range (0, length, 9):
        list_number1.append (list_message[i])
    soup = BeautifulSoup (str (list_number1), 'lxml')
    list_number = soup.getText ()
    list_number = list_number[1:-1]
    list_number = list_number.split (',')
    return list_number


# get course name
def get_courese_name():
    list_course_name1 = []
    for i in range (1, length, 9):
        list_course_name1.append (list_message[i])
    soup = BeautifulSoup (str (list_course_name1), 'lxml')
    list_course_name = soup.getText ()
    list_course_name = list_course_name[1:-1]
    list_course_name = list_course_name.split (',')
    return list_course_name


# get credit
def get_credit():
    list_credit1 = []
    for i in range (2, length, 9):
        list_credit1.append (list_message[i])
    soup = BeautifulSoup (str (list_credit1), 'lxml')
    list_credit = soup.getText ()
    list_credit = list_credit[1:-1]
    list_credit = list_credit.split (',')
    return list_credit


# get category
def get_category():
    list_category1 = []
    for i in range (3, length, 9):
        list_category1.append (list_message[i])
    soup = BeautifulSoup (str (list_category1), 'lxml')
    list_category = soup.getText ()
    list_category = list_category[1:-1]
    list_category = list_category.split (',')
    return list_category


# get nature
def get_nature():
    list_nature1 = []
    for i in range (4, length, 9):
        list_nature1.append (list_message[i])
    soup = BeautifulSoup (str (list_nature1), 'lxml')
    list_nature = soup.getText ()
    list_nature = list_nature[1:-1]
    list_nature = list_nature.split (',')
    return list_nature


# get assessment
def get_Assessment():
    list_Assessment1 = []
    for i in range (5, length, 9):
        list_Assessment1.append (list_message[i])
    soup = BeautifulSoup (str (list_Assessment1), 'lxml')
    list_Assessment = soup.getText ()
    list_Assessment = list_Assessment[1:-1]
    list_Assessment = list_Assessment.split (',')
    return list_Assessment


# get mode
def get_mode():
    list_mode1 = []
    for i in range (6, length, 9):
        list_mode1.append (list_message[i])
    # list_mode = re.findall(re.compile('<td.*?center;">(.*?)</td>', re.S), str(list_mode1))
    soup = BeautifulSoup (str (list_mode1), 'lxml')
    list_mode = soup.getText ()
    list_mode = list_mode[1:-1]
    list_mode = list_mode.split (',')
    return list_mode


# get score
def get_score():
    list_score1 = []
    for i in range (7, length, 9):
        list_score1.append (list_message[i])
    # list_score = re.findall(re.compile('<td.*?right;">(.*?)</td>', re.S), str(list_score1))
    soup = BeautifulSoup (str (list_score1), 'lxml')
    list_score = soup.getText ()
    list_score = list_score[1:-1]
    list_score = list_score.split (',')
    return list_score


# logout user
def logout():
    url1 = 'http://jwxt.dgut.edu.cn/dglgjw/DoLogoutServlet'
    # urlw = 'http://jwxt.dgut.edu.cn/dglgjw/MainFrm.html'
    # response4 =s.get(urlw,headers = headers)
    # response4.encoding='gb2312'
    # log(response4.text)
    # log("退出后")
    try:
        response3 = s.get (url1, headers=config.headers)
        log (response3.status_code)
        log ("logout success")
    except Exception:
        log ("异常")


if __name__ == '__main__':
    direct_url = get_redirect_url ()
    try:
        response1 = s.get (direct_url, headers=config.header1)
        response1.encoding = 'gb2312'
    except Exception:
        log ("异常捕捉")
    time.sleep (2)  # sleep 2S
    html = get_html ()
    # get personal information and printing time
    req = re.compile (r'.*?<div style="float:left;text-align:left;width:.*?">(.*?)</div>', re.S)
    list = re.findall (req, html)
    log (list)

    # get Display column information
    list_play = []
    soup = BeautifulSoup (html, "lxml")
    for i, child in enumerate (soup.thead.children):
        list_play.append (child)
    # log(list1)
    req1 = re.compile (r'<td width=".*?">(.*?)</td>', re.S)
    list_plays = re.findall (req1, str (list_play))
    list_plays = list_plays[0:-1]  # remove 备注
    list_message = []
    for i in soup.find_all ('td'):
        list_message.append (i)

    # get each td tag
    list_message = list_message[10:]  # remove redundant information
    # log(list_message)
    length = len (list_message)  # length of list_message

    # related information list
    list_number = get_number ()
    list_get_course_name = get_courese_name ()
    list_credit = get_credit ()
    list_category = get_category ()
    list_nature = get_nature ()
    list_Assessment = get_Assessment ()
    list_mode = get_mode ()
    list_socer = get_score ()

    # file path
    file_path = "H:\\flask\\1.xlsx"
    wirte_file (file_path)
    time.sleep (2)
    # logout
    logout ()
