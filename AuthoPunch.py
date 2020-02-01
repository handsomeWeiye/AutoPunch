import requests
from bs4 import BeautifulSoup
import re
import sys
import io
from requests.packages import urllib3
import time
import datetime



urllib3.disable_warnings()








def main(userName,password,userId,phone,province,city,area):



    def log(string):
        now = time.strftime('%Y.%m.%d %H:%M:%S ',time.localtime(time.time()))
        with open('log.txt','a+',encoding="utf-8")as f:
            f.write(now + string + "\n")
        print(string)


    def login(session,loginUrl,header,loginData,userName,password):

        def getCookies():
            #获取cookies数据并格式化
            try:
                cookiesStr = "zcas=;" + "ASPSESSIONIDASFCRCSB" +"=" + r.cookies['ASPSESSIONIDASFCRCSB'] 
                log("得到cookies"+" "+cookiesStr)
                return cookiesStr
            except:
                cookiesStr = "zcas=;" + "ASPSESSIONIDCWBDRCTA" +"=" + r.cookies['ASPSESSIONIDCWBDRCTA'] 
                log("得到cookies"+" "+cookiesStr)
                return cookiesStr
        def getCheckCode(r):
            try:
                # 使用css选择器解析页面，解析验证码
                soup = BeautifulSoup(r.text, "lxml")
                checkStr = soup.select("#form > div:nth-child(3)")
                checkNum = re.search(r'\d{4}', str(checkStr)).group(0)
                # log
                log("获取到验证码{}".format(checkNum))
                return checkNum
            except:
                log("获取验证码失败")
                return None

        def getHeader(r):



            try:
                cookies = getCookies()
                header['Cookie'] = cookies
                log("公用请求头制作完成")
                return header
            except:
                log("制作请求头出现错误")
                return None


        def getLoginData(r):
            try:
                # 构建login请求所需要的表单
                loginData['code'] = getCheckCode(r)
                loginData['username'] = userName
                loginData['userpwd'] = password
                log("登录表单制作完成")
                return loginData   
            except:
                log("登录表单出现错误")
                return None


        try:
            # 获取header和login表单
            r = session.get(loginUrl, verify=False)
            header = getHeader(r)
            loginData = getLoginData(r)
            # 发送登录页面请求
            loginResponse = session.post(loginUrl, data=loginData,headers=header, allow_redirects = False)
            # print(loginResponse.status_code)
            if(loginResponse.status_code == 302):
                log("登录成功") 
        except:
            log("登录不成功")   
            

    def punch(session,addUrl,userId,infoData,header):
        #日期模块

        def getDay():
            nowDate = str(datetime.date.today()).split('-')
            month = nowDate[1][1]
            day = nowDate[2]
            if(day[0]=="0"):
                day = day[1]
            nowDate = "2020年" +  month + "月" + day + "日"
            log("日期生成成功，目前的日期为{}".format(nowDate))
            
            return nowDate

        nowDate = getDay()
        url =  addUrl + "?id=" + userId + "&id2=" + nowDate
        addResponse = session.post(url, data=infoData,headers=header, verify=False)
        if (addResponse.status_code == 200):
            log("打卡成功")
        else:
            log("打卡失败")


    # 首先设置模拟登录所需要的变量

    loginUrl = 'https://xsswzx.cdu.edu.cn:81/cp/com_user/weblogin.asp'
    addUrl = "https://xsswzx.cdu.edu.cn:81/cp/com_user/project_add.asp"

    chackNum = ''
    cookiesStr = ''



    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://xsswzx.cdu.edu.cn:81/cp/com_user/weblogin.asp",
        "Origin": "https://xsswzx.cdu.edu.cn:81",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.9,zh-HK;q=0.8,zh-CN;q=0.7,zh;q=0.6,en-US;q=0.5",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Length": "104",
        "Cookie": "",
        "Host": "xsswzx.cdu.edu.cn:81",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }

    loginData = {
        "username": userName,
        "userpwd": password,
        "code": "",
        "login": "login",
        "checkcode": "1",
        "rank": "0",
        "action": "login",
        "m5": "1",
    }

    infoData = {
        "stu_no":userName,
        "stu_phone":phone,
        "province":province,
        "city":city,
        "area":area,
        "wuhan":"否",
        "keshou":"否",
        "fare":"否",
        "fanxiao":"否",
        "fanxiaodata":"2020-02-23",
        "Submit":"提交",
        "actinon":"add",
        "class_id":"399",
        "college_code":"sxy845"
    }


    # 开启一个session,登录且打卡
    session = requests.Session()
    login(session,loginUrl,header,loginData,userName,password)
    punch(session,addUrl,userId,infoData,header)






if __name__ == "__main__":
    main("201711533704","CDU201711533704","047daa3a31440fa7c66e8c2ee334230674081b616d41","19102688475","山西省","晋中市","太谷县")
    main("201610811129","CDU201610811129","ce605f41d7140ea313d266c18332216222583610eb50","15102870927","四川省","泸州市","泸县")
    



