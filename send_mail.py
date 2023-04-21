# coding: utf-8

import smtplib  # 加载smtplib模块
from datetime import timezone, timedelta, datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from pyhocon import ConfigFactory

SHA_TZ = timezone(
    timedelta(hours=8),
    name='Asia/Shanghai',
)

# 协调世界时
utc_now = datetime.utcnow().replace(tzinfo=timezone.utc)
# 北京时间
beijing_now = utc_now.astimezone(SHA_TZ)


class SendMail(object):
    def __init__(self, content, password=None):
        self.content = content  # 发送内容
        self.sender = 'caoqianghappy@126.com'  # 发送地址
        self.sys_sender = 'caoqianghappy@126.com'
        self.sys_pwd = password  # 系统账户密码
        self.title = 'Telegram的聊天记录-' + beijing_now.strftime('%Y-%m-%d %H:%M:%S')  # 标题

    def send(self, file_list):
        """
        发送邮件
        :param file_list: 附件文件列表
        :return: bool
        """
        try:
            # 创建一个带附件的实例
            msg = MIMEMultipart()
            # 发件人格式
            msg['From'] = self.sys_sender
            # 收件人格式
            msg['To'] = self.sender
            # 邮件主题
            msg['Subject'] = self.title

            # 邮件正文内容
            msg.attach(MIMEText(self.content, 'plain', 'utf-8'))

            # 多个附件
            for file_name in file_list:
                print("file_name", file_name)
                # 构造附件
                xlsxpart = MIMEApplication(open(file_name, 'rb').read())
                # filename表示邮件中显示的附件名
                xlsxpart.add_header('Content-Disposition', 'attachment', filename='%s' % file_name)
                msg.attach(xlsxpart)

            # SMTP服务器
            server = smtplib.SMTP_SSL("smtp.126.com", 465, timeout=10)
            # 登录账户
            server.login(self.sys_sender, self.sys_pwd)
            # 发送邮件
            server.sendmail(self.sys_sender, [self.sender, ], msg.as_string())
            # 退出账户
            server.quit()
            return True
        except Exception as e:
            print(e)
            return False


if __name__ == '__main__':
    conf = ConfigFactory.parse_file('default.conf')
    email_password = conf.get_string('info.email_password')
    # 发送内容
    content = "2019-11-01 ~ 2019-11-30 统计，见附件!"
    # 附件列表
    file_list = ["default.conf"]
    ret = SendMail(content, email_password).send(file_list)
    print(ret, type(ret))
