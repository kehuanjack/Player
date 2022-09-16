import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from email.header import Header

def creat(): # 创建附件，把要发的附件放到附件文件夹内统一上传
    global msg
    dir_path = input("附件的文件夹路径(例如：.\dir)：")+"\\"
    for i in os.listdir(dir_path):
        att = MIMEText(open(dir_path+i, 'rb').read(), 'base64', 'utf-8')
        att["Content-Type"] = 'application/octet-stream'
        att["Content-Disposition"] = "attachment; filename=%s"%Header('%s'%i,'utf-8').encode('utf-8')
        msg.attach(att)

def send(user_name=None,user_email=None,title=None,txt=None):
    global msg
    msg = MIMEMultipart()
    msg['From'] = formataddr([my_name,my_email])
    msg['To'] =  formataddr([user_name,user_email])
    msg['Subject'] = title
    msg.attach(MIMEText(txt, 'plain', 'utf-8'))
        
    judge = input("是否要上传附件？(y/n):")
    if judge == 'y':
        creat()

    try:
        smtpObj = smtplib.SMTP_SSL('smtp.qq.com',465)  # 更安全
        #smtpObj = smtplib.SMTP("smtp.qq.com",25)
        smtpObj.login(my_email,my_pass)
        smtpObj.sendmail(my_email, [user_email,], msg.as_string())
        smtpObj.quit()
        print ("邮件发送成功")
    except smtplib.SMTPException:
        print ("Error: 无法发送邮件")    

if __name__ == "__main__":
'''
1.这里只用QQ邮箱，也可以通过修改代码来适用于其他邮箱。
2.把要上传的附件统一放入一个文件夹，然后填入该文件夹路径即可。
3.QQ邮箱授权码获取方式：http://t.csdn.cn/vSSSr。
4.使用前请先把下列内容补充完整。

'''
    
    my_name = "xxx"  # 你的昵称
    my_email= "xxx@qq.com"   # 你的邮箱
    my_pass = "xxx"  # qq邮箱授权码
    
    while(1):
        hhh = input("请依次输入收件人昵称、收件人邮箱、邮件主题、邮件内容：\n").split()
        if len(hhh)==4:
            break
        else:
            print("输入有误，请重新输入")
            
    send(hhh[0],hhh[1],hhh[2],hhh[3])
