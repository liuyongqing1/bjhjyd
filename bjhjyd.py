#-*- coding:utf8 -*-
# import json

import requests,re
from pyquery import PyQuery as pq
from damatuWeb import *
from urllib.parse import quote,unquote

class BJ_YH():
    def __init__(self,Phone_Num,Password):
        self.Phone_NUM=Phone_Num
        self.Password=Password
        self.r=requests.session()
        self.r.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
               'Referer':'https://www.bjhjyd.gov.cn/'}
        self.login_url='https://apply.bjhjyd.gov.cn/apply/user/person/login.html'

    def __str__(self):
        return  self.Resolv_html()

    def SAVE_FILE(self):
        Url_File='https://apply.bjhjyd.gov.cn/apply/validCodeImage.html?ee=1'
        with open('code.png','wb') as f:
            File_data=self.r.get(Url_File)
            f.write(File_data.content)
            f.close()

    def LOGIN(self):
        self.SAVE_FILE()
        vcode=input('打开 code.png 输入图片中的验证码: ') #如果需要手动输入验证码，需要取消注释。
        # vcode=dmt.decode('code.png', 101) #如果需要手动输入验证码，需要注释本行
        print(vcode)
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
        code=re.compile(r'message=.*?$')
        codestatus=re.findall(code,resurl)[0]
        codestatus=unquote(codestatus)
        if codestatus == 'message=验证码错误':
            print('错误的验证码,已向平台报告，不扣积分')
            dmt.reportError('894657096')                #如果需要手动输入验证码，需要注释。
            self.LOGIN()
        elif codestatus == 'message=建议您使用IE8及以上版本的浏览器，其他浏览器对小客车系统兼容性不完善！':
            return result.text
        else:
            print(codestatus)
            exit(2)

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
    dmtuser='打码兔平台用户名'      #如果需要手动输入验证码，需要注释本行
    dmtpassword='打码兔平台密码'  #如果需要手动输入验证码，需要注释本行
    phone='摇号平台用户名'
    password='摇号平台密码'
    dmt = DamatuApi(dmtuser, dmtpassword)  #如果需要手动输入验证码，需要注释本行
    print('当前剩余积分：{}'.format(dmt.getBalance())) #如果需要手动输入验证码，需要注释本行
    yh=BJ_YH(phone,password)
    print(yh)