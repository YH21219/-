import requests,re


__author__ ='YH'
__date__='2018.5.10'


"""
模拟登录教务处
爬取成绩
"""


#代替print输出
def log(*args,**kw):
    print(*args,**kw)


#模拟登录
s= requests.session()
#目标网站
URL = 'https://cas.dgut.edu.cn/home/Oauth/getToken/appid/jwxt.html'


def get_direct_url():
    header = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Host': 'cas.dgut.edu.cn',
        'Origin': 'https://cas.dgut.edu.cn',
        'Referer': 'https://cas.dgut.edu.cn/home/Oauth/getToken/appid/jwxt.html',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:58.0) Gecko/20100101 Firefox/58.0',
        'X-Requested-With': 'XMLHttpRequest',
    }
    res = s.get(URL, headers=header)
    req = re.compile(r'<script>.*?var.*?token.*?"(.*?)".*?</script>', re.S)
    items = re.findall(req, res.text)
    str = items[0]
    data = {
        'username': '×××',
        'password': '×××',
        '__token__': str
    }
    response = s.post(URL, headers=header, allow_redirects=False, data=data)
    log(response.text)
    req1 = re.compile(r'.*?token=(.*?)\\', re.S)
    items1 = re.findall(req1, response.text)
    log(items1[0])
    token = items1[0]
    url1 = 'http://jwxt.dgut.edu.cn/dglgjw/login?token=' + token
    return url1



if __name__ == '__main__':
    header1 = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',
        'Host': 'jwxt.dgut.edu.cn',
    }
    direct_url = get_direct_url()
    response1 = s.get(direct_url,headers=header1)
    response1.encoding = 'gb2312'
    #log(response1.text)
    url = 'http://jwxt.dgut.edu.cn/dglgjw/student/xscj.stuckcj_data.jsp'
    header2={
        'Connection': 'keep-alive',
        'Host': 'jwxt.dgut.edu.cn',
        'Origin': 'http://jwxt.dgut.edu.cn',
        'Referer': 'http://jwxt.dgut.edu.cn/dglgjw/student/xscj.stuckcj.jsp?menucode=JW130706',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.170 Safari/537.36',

    }
    form_data={
        'sjxz': 'sjxz3',
        'ysyx': 'yscj',
        'zx':'1',
        'fx':'1',
        'userCode': '201500002979',
        'xypjwchcnckcj': '0',
        'pjwchckcjklpbcj': '0',
        'xn': '2017',
        'xn1': '2018',
        'xq':'0',
        'ysyxS': 'on',
        'sjxzS': 'on',
        'zxC': 'on',
        'fxC': 'on',
        'menucode_current':'',
    }
    response2 = s.post(url,headers = header2,data= form_data)
    log(response2.text)
