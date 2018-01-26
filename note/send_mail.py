# -*- coding:utf-8 -*-
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText

# 第三方服务
mail_host = 'smtp.ym.163.com'
mail_user = 'xxx'
mail_pass = 'xxx'

# sendu
sender = 'xxxxx'
receivers = ['xxxx', 'xxxx']


def send_mail(content, subject):
    smtp = SMTP_SSL(mail_host)
    smtp.set_debuglevel(1)
    smtp.ehlo(mail_host)
    smtp.login(mail_user, mail_pass)
    msg = MIMEText('<html><h3>{0}</h3></html>'.format(content), 'html', 'utf-8')
    msg["Subject"] = Header(subject, 'utf-8')
    smtp.sendmail(sender, receivers, msg.as_string())
    smtp.quit()


if __name__ == '__main__':
    pass
#    send_mail('断网', 'error')
