#-*- coding:utf8 -*-
# import json

import requests,re
from pyquery import PyQuery as pq
from damatuWeb import *

class BJ_YH():
    def __init__(self,Phone_Num,Password):
        self.Phone_NUM=Phone_Num
        self.Password=Password
        self.r=requests.session()
        self.r.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               'Referer':'https://www.bjhjyd.gov.cn/'}
        self.login_url='https://apply.bjhjyd.gov.cn/apply/user/person/login.html'

    def SAVE_FILE(self):
        Url_File='https://apply.bjhjyd.gov.cn/apply/validCodeImage.html?ee=1'
        with open('code.png','wb') as f:
            File_data=self.r.get(Url_File)
            f.write(File_data.content)
            f.close()

    def LOGIN(self):
        self.SAVE_FILE()
        vcode=dmt.decode('code.png', 101)
        # print(vcode)
        data={
            'userType':0,
            'ranStr':None,
            'userTypeSelect':0,
            'serviceType':'1',
            'personMobile':self.Phone_NUM,
            'loginType':'mobile',
            'unitLoginTypeSelect':'0',
            'unitMobile':None,
            'orgCode':None,
            'password':self.Password,
            'pin':None,
            'validCode':vcode
        }
        result=self.r.post(self.login_url,data=data)
        result.encoding = 'utf-8'
        resurl=result.url
        code=re.compile(r'.*?%E9%AA%8C%E8%AF%81%E7%A0%81%E9%94%99%E8%AF%AF')
        codestatus=re.match(code,resurl)
        # print(resurl)
        if codestatus:
            print('错误的验证码,已向平台报告，不扣积分')
            dmt.reportError('894657096')
            exit(2)
        return result.text

    def Resolv_html(self):
        RESULT=[]
        html = pq(self.LOGIN())
        LISTINFO = html.find('.yhzx_btn').eq(1)
        for i in LISTINFO.items():
            TABLE = i.find('table').attr('class')
            INFO = i.find('.%s tbody' % TABLE)
            NAME = INFO.find('td:nth-child(2)').text()
            ID = INFO.find('td:nth-child(1)').text()
            REQDATE = INFO.find('td:nth-child(5)').text()
            STATUS = INFO.find('td:nth-child(7)').text()
            SHSTATUS='姓名：%3s , 申请编号：%10s , 申请日期：%10s   审核状态：%3s' % (NAME, ID, REQDATE, STATUS)
            RESULT.append(SHSTATUS)
        try:
            return '\n'.join(RESULT)
        except Exception as f:
            raise f


if __name__ == '__main__':
    dmtuser='输入打码兔用户名'
    dmtpassword='请输入打码兔密码'
    dmt = DamatuApi(dmtuser, dmtpassword)
    print(dmt.getBalance())
    phone='北京摇号平台手机号'
    password='北京摇号平台密码'
    yh=BJ_YH(phone,password)
    print(yh.Resolv_html())