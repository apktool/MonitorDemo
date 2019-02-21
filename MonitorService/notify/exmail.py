from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib


class exmail(object):
    def __init__(self, mail_config):
        self.from_addr = mail_config['from_addr']
        self.password = mail_config['password']
        self.to_addr = mail_config['to_addr']
        self.smtp_server = mail_config['smtp_server']
        self.smtp_port = int(mail_config['smtp_port'])

    def send(self,
             title,
             message,
             sender_nickname='frontsurf',
             receiver_nickname='frontsurf'):

        lam_format_addr = lambda name, addr: formataddr((Header(name, 'utf-8').encode(), addr))

        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = lam_format_addr(sender_nickname, self.from_addr)
        msg['To'] = lam_format_addr(receiver_nickname, self.to_addr)
        msg['Subject'] = Header(title, 'utf-8').encode()

        server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
        server.login(self.from_addr, self.password)

        server.sendmail(self.from_addr, [self.to_addr], msg.as_string())
        server.quit()


if __name__ == '__main__':
    # https://www.jianshu.com/p/d5d9e52d6d2d
    mail_config = {
        'from_addr': 'apktoolOo@gmail.com',
        'password': 'NjFGTQcXGyHrggoT',
        'to_addr': 'apktoolOo@gmail.com',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': int('465')
    }

    exmail = exmail(mail_config)
    exmail.send("test", "Hello world")
