import smtplib
from email.mime.text import MIMEText
from email.header import Header
# My own QQ SMTP service
def send_code(address, code):
    from_addr = '1709754403@qq.com'
    password = 'oxzuvolodrzpcgad'
    smtp_server = 'smtp.qq.com'
    msg = MIMEText('Dear User,\n\n\tYour verification code is: '+code+'\n\nSincerely,\nhaeChat', 'plain', 'utf-8')
    msg['From'] = Header('haeChat')
    msg['To'] = Header(address)
    msg['Subject'] = Header('haeChat Verification Code')
    server = smtplib.SMTP_SSL(smtp_server)
    server.connect(smtp_server, 465)
    server.login(from_addr, password)
    server.sendmail(from_addr, address, msg.as_string())
    server.quit()
