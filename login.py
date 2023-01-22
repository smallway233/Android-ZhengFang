# -*- coding=utf-8 -*-

from email import message
from http.client import responses
from msilib.schema import tables
from webbrowser import get
import requests
import time
from lxml import etree
from hex2b64 import HB64
import RSAJS
import lxml
import bs4

class Longin():

    def __init__(self,user,password,login_url,login_KeyUrl):
        # 初始化程序数据
        self.Username = user
        self.Password = password
        nowTime = lambda:str(round(time.time()*1000))
        self.now_time = nowTime()

        self.login_url = login_url
        self.login_Key = login_KeyUrl
    def Get_indexHtml(self):
        # 获取教务系统网站
        self.session = requests.Session()
        self.session.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Referer": self.login_url+ self.now_time,
    "Upgrade-Insecure-Requests": "1"
})
        self.response = self.session.get(self.login_url+ self.now_time).content.decode("utf-8")

    def Get_csrftoken(self):
        # 获取到csrftoken
        lxml = etree.HTML(self.response)
        self.csrftoken = lxml.xpath("//input[@id='csrftoken']/@value")[0]

    def Get_PublicKey(self):
        # 获取到加密公钥
        key_html = self.session.get(self.login_Key + self.now_time)
        key_data = key_html.json()
        self.modulus = key_data["modulus"]
        self.exponent = key_data["exponent"]

    def Get_RSA_Password(self):
        # 生成RSA加密密码
        rsaKey = RSAJS.RSAKey()
        rsaKey.setPublic(HB64().b642hex(self.modulus),HB64().b642hex(self.exponent))
        self.enPassword = HB64().hex2b64(rsaKey.encrypt(self.Password))

    def Longin_Home(self):
        # 登录信息门户,成功返回session对象
        self.Get_indexHtml()
        self.Get_csrftoken()
        self.Get_PublicKey()
        self.Get_RSA_Password()
        login_data = [("csrftoken", self.csrftoken),("yhm", self.Username),("mm", self.enPassword),("mm", self.enPassword)]
        login_html = self.session.post(self.login_url + self.now_time,data=login_data)
        # 当提交的表单是正确的，url会跳转到主页，所以此处根据url有没有跳转来判断是否登录成功
        if login_html.url.find("login_slogin.html") == -1: # -1没找到，说明已经跳转到主页
            return self.session
        else:
            return False

class TimeTable():
    def run(year,data,session,table_url):
        data = {"xnm":year,"xqm":data}
        table_info = session.post(table_url,data = data).json()
        # print(table_info)
        plt = '"xm":{0},"kcmc":"{1}","cj":"{2}","jd":"{3}"'
        F=[]
        for each in table_info["items"]:
            a=  {"xm":each["xm"],"kcmc":each["kcmc"],"cj":each["cj"],"jd":each["jd"]}
            F.append(a)
        F=str(F)
        return F


class TimeTable2():
    def run(url,session):
        F=[]
        data={"xnm":"2022","xqm":"3","xnmc":"2022-2023","xqmmc":"1","xqh_id":"1","njdm_id":"2021","zyh_id":"C42830794E000443E055000000000001","bh_id":"212040101","tjkbzdm":"1","tjkbzxsdm":"0","zymc":"大数据技术T"}
        a=session.post(url,data=data).json()
        print(a['kbList'])
        a=a['kbList']
        for list in a:
            c=  {"kcmc":list['kcmc'],"js":list['cdmc'],"zs":list['zcd'],"jsxm":list['xm'],"js":list['jcor'],"xqj":list['xqj'],}
            F.append(c)
        return F
    

    def run2(year,data,session,table_url):
        data = {"xnm":year,"xqm":data,"queryModel.showCount":20}
        table_info = session.post(table_url,data = data).json()
        # print(table_info)
        plt = '"xm":{0},"kcmc":"{1}","cj":"{2}","jd":"{3}"'
        F=[]
        for each in table_info["items"]:
            a=  {"xm":each["xm"],"kcmc":each["kcmc"],"cj":each["cj"],"jd":each["jd"]}
            F.append(a)
        # F=str(F)
        return table_info



class 年级():
    def run(url,session):
        data={"姓名":"","年级":"","身份证号":"","学院":"","班级名称":"","民族":"","政治面貌":"","性别":""}
        res=session.get(url)
        soup=bs4.BeautifulSoup(res.text,"lxml")
        a = soup.find_all('div', id="col_njdm_id")
        for b in a:
            b=b.get_text()
            b=b.strip()
            data['年级']=b
        a = soup.find_all('div', id="col_xm")
        for b in a:
            b=b.get_text()
            b=b.strip()
            data['姓名']=b
        a = soup.find_all('div', id="col_zjhm")
        for b in a:
            b=b.get_text()
            b=b.strip()
            data['身份证号']=b
        a = soup.find_all('div', id="col_jg_id")
        for b in a:
            b=b.get_text()
            b=b.strip()
            data['学院']=b
        a = soup.find_all('div', id="col_bh_id")
        for b in a:
            b=b.get_text()
            b=b.strip()
            data['班级名称']=b
        a = soup.find_all('div', id="col_mzm")
        for b in a:
            b=b.get_text()
            b=b.strip()
            data['民族']=b
        a = soup.find_all('div', id="col_zzmmm")
        for b in a:
            b=b.get_text()
            b=b.strip()
            data['政治面貌']=b
        a = soup.find_all('div', id="col_xbm")
        for b in a:
            b=b.get_text()
            b=b.strip()
            data['性别']=b
        return data

def get_table():
    login_url = "http://jxgl.csiic.com/jwglxt/xtgl/login_slogin.html?language=zh_CN&_t="

    login_KeyUrl = "http://jxgl.csiic.com/jwglxt/xtgl/login_getPublicKey.html?time="

    a = " http://jxgl.csiic.com/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdm=N305005"

    b="http://jxgl.csiic.com/jwglxt/kbdy/bjkbdy_cxBjKb.html?gnmkdm=N214505"

    个人信息="http://jxgl.csiic.com/jwglxt/xsxxxggl/xsgrxxwh_cxXsgrxx.html?gnmkdm=N100801&layout=default&su="

    zspt = Longin("账号", "密码", login_url, login_KeyUrl)
    response = zspt.Longin_Home()
    
    table=TimeTable2.run2(year="2021",data="12",session=response,table_url=a)
    information=年级.run(个人信息,response)
    print(information)

if __name__=="__main__":
    get_table()
