from email.mime.text import MIMEText

import time


def envoyer_email(contenu, sujet = 'Récupération de prix 100%',from_addr = 'jxlnxhc@gmail.com', password = 'shuaige@123',to_addrs = ['hxu@auchan.fr'],smtp_server='smtp.gmail.com'):
    msg = MIMEText(contenu, 'plain', 'utf-8')
    runtime = time.strftime("%d/%m/%Y", time.localtime())
    msg['Subject'] = sujet + runtime
    import smtplib
    server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
    # server.connect("smtp.auchan.com",465)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(from_addr, password)
    for to_addr in to_addrs:
        server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()