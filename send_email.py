import smtplib
from email.header import Header  # 用来设置邮件头和邮件主题
from email.mime.text import MIMEText  # 发送正文只包含简单文本的邮件，引入MIMEText即可
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from pyhocon import ConfigFactory

SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)

# 协调世界时
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
# 北京时间
beijing_now = utc_now.astimezone(SHA_TZ)

# 发件人和收件人
sender = 'caoqianghappy@126.com'
receiver = 'caoqianghappy@126.com'

# 所使用的用来发送邮件的SMTP服务器
smtpServer = 'smtp.126.com'

# 发送邮箱的用户名和授权码（不是登录邮箱的密码）
username = 'caoqianghappy@126.com'

mail_title = 'Telegram的聊天记录-' + beijing_now.strftime('%Y-%m-%d %H:%M:%S')


def send(mail_body="这里是邮件的正文", password=None):
    # 创建一个实例
    message = MIMEText(mail_body, 'plain', 'utf-8')  # 邮件正文
    message['From'] = sender  # 邮件上显示的发件人
    message['To'] = receiver  # 邮件上显示的收件人
    message['Subject'] = Header(mail_title, 'utf-8')  # 邮件主题

    try:
        smtp = smtplib.SMTP()  # 创建一个连接
        smtp.connect(smtpServer)  # 连接发送邮件的服务器
        smtp.login(username, password)  # 登录服务器
        smtp.sendmail(sender, receiver, message.as_string())  # 填入邮件的相关信息并发送
        print("邮件发送成功！！！")
        smtp.quit()
    except Exception as e:
        print(e, type(e))
        print("邮件发送失败！！！")


if __name__ == '__main__':
    conf = ConfigFactory.parse_file('default.conf')
    email_password = conf.get_string('info.email_password')
    send("测试", email_password)
