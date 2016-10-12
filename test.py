# coding= utf-8

from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import time
import requests
from requests.utils import dict_from_cookiejar
from brand.ProxyConf import ProxyConf, key1 as app_key
from brand.QuanWangProxy import get_proxy
import re

# a = "第  页 共 6573 页 78876 条数据"
# print len(a)
# print a[2]
# print a.replace(" ", '')
# print re.split('\?+', a)

# r = session.get("http://1212.ip138.com/ic.asp", headers=headers, proxies=proxy_config.get_proxy())
# r.encoding = 'gbk'
# print r.text





# from_addr = 'liuwenhai0425@126.com'
# password = '19901125'
# to_addr = '1262437143@qq.com'
# smtp_server = 'smtp.126.com'
#
# msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
# msg['From'] = _format_addr('Python爱好者 <%s>' % from_addr)
# msg['To'] = _format_addr('管理员 <%s>' % to_addr)
# msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()
# print msg
#
# server = smtplib.SMTP(smtp_server, 25)
# # server.set_debuglevel(1)
# server.login(from_addr, password)
# server.sendmail(from_addr, [to_addr], msg.as_string())
# server.quit()

