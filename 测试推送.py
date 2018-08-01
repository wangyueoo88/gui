import requests
import datetime
import re
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import multiprocessing
now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=1)
todaytime=now.strftime("%Y-%m-%d")
yestime=yesterday.strftime("%Y-%m-%d")
list_name=[]
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
class Tuisong():
    def __init__(self,id,email,todaytime=todaytime):
        self.email=email
        self.time_today=todaytime
        self.header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36'}
        self.starttime='2018-06-01'
        self.yestime=yestime
        self.id=id
        self.from_addr = ''
        self.password = ''
        self.smtp_server = 'smtp.163.com'
        self.smtp_port='25'
    def get_url(self):
        url='http://10.10.10.10/workerlog/query?deviceId=1&userId={}&startTimeStr={}+00%3A00%3A00&endTimeStr={}+00%3A00%3A00'.format(self.id,self.starttime,self.time_today)
        return url
    def parase_html(self,url):
        response = requests.get(url,headers=self.header).text
        return response

    def deal_data(self,content):
        name = re.search(r'name":"(.*?)"', content).group(1)
        timerule=re.compile(self.yestime+r'(.*?)"')
        timerulep=re.compile('2018-7-10(.*?)"')
        cc = re.findall(timerule, content)
        num=len(cc)
        if num==0:
            mes='%s,你%s未打卡，记得补打卡'%(name,self.yestime)
        elif num==1:
            mes='%s,你%s打卡1次，记得补打卡'%(name,self.yestime)
        else:
            mes='%s ,你%s的打卡次数为%d次 分别为 %s'%(name,self.yestime,num,str(cc))
        return mes
    def sendemail(self,email,content):

        # 输入收件人地址:
        to_addr = email
        # 输入SMTP服务器地址:
        msg = MIMEText(content, 'plain', 'utf-8')
        msg['From'] = _format_addr('打卡提醒 <%s>' % self.from_addr)
        msg['To'] = _format_addr('管理员 <%s>' % to_addr)
        msg['Subject'] = Header('打卡提醒', 'utf-8').encode()
        server = smtplib.SMTP(self.smtp_server, 25)  # SMTP协议默认端口是25
        server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        server.sendmail(self.from_addr,to_addr, msg.as_string())
        server.quit()

    def run(self):
        print(self.deal_data(self.parase_html(self.get_url())))
        self.sendemail(self.email,self.deal_data(self.parase_html(self.get_url())))

def main():
    ex()
def ex():
    mmm=1
    for i in list_name:
        i[0]=Tuisong(i[1],i[2])
        i[0].run()
        print('--------推送第%d次--------------'%mmm)
        mmm+=1

if __name__ == '__main__':
    main()