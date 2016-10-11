# coding= utf-8

from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr
import smtplib
import time
import requests
from brand.ProxyConf import ProxyConf, key1 as app_key


proxy_config = ProxyConf(app_key)
headers = dict()
headers['Proxy-Authorization'] = proxy_config.get_auth_header()
url = "http://www.pss-system.gov.cn/sipopublicsearch/patentsearch/showAbstractInfo-viewAbstractInfo.shtml"
params = {'nrdAn': "CN201610522240",
          'cid': "CN201610522240.720160928FM",
          'sid': "CN201610522240.720160928FM",
          'wee.bizlog.modulelevel': "0201101"}
r = requests.post(url, params=params, headers=headers, proxies=proxy_config.get_proxy())
r.encoding = 'utf-8'
print r.text




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

